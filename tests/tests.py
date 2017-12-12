
from datetime import timedelta, datetime
from time import sleep

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from django_timer.models import Timer, Segment, TimerException

class ModelTest(TestCase):

    def test_create_timer_with_segment(self):
        timer = Timer.objects.start()
        self.assertEqual(timer.segment_set.count(), 1)
        self.assertIsInstance(timer.segment_set.first().start_time, datetime)

    def test_duration_if_timer_still_running(self):
        timer = Timer.objects.start()
        d1 = timer.duration()
        sleep(0.01)
        d2 = timer.duration()
        self.assertTrue(d2>d1)

    def test_stop_timer(self):
        timer = Timer.objects.start()
        timer.stop()
        self.assertIsInstance(timer.segment_set.first().stop_time, datetime)
        self.assertIsInstance(timer.segment_set.last().duration(), timedelta)
        self.assertIsInstance(timer.duration(), timedelta)

    def test_pause_timer(self):
        timer = Timer.objects.start()
        timer.pause()
        self.assertIsInstance(timer.segment_set.first().stop_time, datetime)
        self.assertIsInstance(timer.duration(), timedelta)

    def test_resume_timer(self):
        timer = Timer.objects.start()
        timer.pause()
        timer.resume()
        # Timer cannot be resumed a second time, if it's still running
        with self.assertRaises(Exception):
            timer.resume()
        self.assertEqual(timer.segment_set.count(), 2)
        self.assertIsNone(timer.segment_set.last().stop_time)
        timer.pause()
        timer.resume()
        self.assertEqual(timer.segment_set.count(), 3)

    def test_timer_stopped(self):
        timer = Timer.objects.start()
        timer.stop()
        with self.assertRaises(TimerException):
            timer.resume()

    def test_with_time(self):
        timer = Timer.objects.start()
        sleep(0.1)
        timer.pause()
        timer.resume()
        sleep(0.1)
        timer.stop()
        self.assertAlmostEqual(timer.duration().total_seconds(), 0.2, delta=0.05)

    def test_with_user(self):
        user = User.objects.create_user(username='foo', password='bar')
        timer = Timer.objects.start(user=user)
        self.assertEqual(timer.user, user)

class ViewTest(TestCase):

    def test_start_and_stop_timer(self):
        response = self.client.post(reverse('start_timer'))
        self.assertEqual(Timer.objects.count(), 1)
        response = self.client.post(reverse('pause_timer'))
        self.assertIsInstance(Timer.objects.first().segment_set.last().stop_time, datetime)
        response = self.client.post(reverse('resume_timer'))
        self.assertEqual(Timer.objects.first().segment_set.count(), 2)
        self.assertIsNone(Timer.objects.first().segment_set.last().stop_time)
        response = self.client.post(reverse('stop_timer'))
        self.assertTrue(Timer.objects.first().stopped)     

    def test_start_timer_as_user(self):
        user = User.objects.create_user(username='foo', password='bar')
        self.client.login(username='foo', password='bar')
        self.client.post(reverse('start_timer'))
        timer = Timer.objects.first()
        self.assertEqual(timer.user, user)
        