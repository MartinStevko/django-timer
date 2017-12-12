
from datetime import timedelta, datetime
from time import sleep

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.template import Template, Context
from django.http import HttpResponseBadRequest
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

    def test_get_or_start(self):
        t1 = Timer.objects.get_or_start()
        self.assertEqual(Timer.objects.count(), 1)
        t2 = Timer.objects.get_or_start()
        self.assertEqual(Timer.objects.count(), 1)
        self.assertEqual(t1.pk, t2.pk)
        t2.stop()
        t3 = Timer.objects.get_or_start()
        self.assertEqual(Timer.objects.count(), 2)
        self.assertNotEqual(t2.pk, t3.pk)
        user = User.objects.create_user(username='foo', password='bar')
        t4 = Timer.objects.get_or_start(user=user)
        self.assertEqual(Timer.objects.count(), 3)
        
    def test_get_for_user(self):
        u1 = User.objects.create_user(username='foo', password='bar')
        u2 = User.objects.create_user(username='bar', password='foo')
        t1 = Timer.objects.get_or_start(user=u1)
        t1.stop()
        t1a = Timer.objects.get_or_start(user=u1)
        t2 = Timer.objects.get_or_start(user=u2)
        t0 = Timer.objects.get_or_start(user=None)
        self.assertEqual(Timer.objects.count(), 4)

        self.assertEqual(Timer.objects.get_for_user(), t0)
        self.assertEqual(Timer.objects.get_for_user(user=u1), t1a)
        self.assertEqual(Timer.objects.get_for_user(user=u2), t2)

        t2.stop()
        with self.assertRaises(ObjectDoesNotExist):
            Timer.objects.get_for_user(user=u2)

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

class TemplateTagsTest(TestCase):

    def test_render_timer(self):
        timer = Timer.objects.start()
        template = Template('{% load timer %}{% render_timer timer %}')
        context = Context({'timer': timer})
        html = template.render(context)
        self.assertIn('id="django-timer"', html)
        