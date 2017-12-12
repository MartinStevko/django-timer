
from datetime import timedelta, datetime

from django.test import TestCase
from django.urls import reverse

from django_timer.models import Timer, Segment

class ModelTest(TestCase):

    def test_create_timer_with_segment(self):
        timer = Timer.objects.start_timer()
        self.assertEqual(timer.segment_set.count(), 1)
        self.assertIsInstance(timer.segment_set.first().start_time, datetime)

    def test_stop_timer(self):
        timer = Timer.objects.start_timer()
        timer.stop()
        self.assertIsInstance(timer.segment_set.first().stop_time, datetime)
        self.assertIsInstance(timer.segment_set.last().duration(), timedelta)
        self.assertIsInstance(timer.duration(), timedelta)

    def test_pause_timer(self):
        timer = Timer.objects.start_timer()
        timer.pause()
        self.assertIsInstance(timer.segment_set.first().stop_time, datetime)
        self.assertIsInstance(timer.duration(), timedelta)

    def test_resume_timer(self):
        timer = Timer.objects.start_timer()
        timer.pause()
        timer.resume()
        self.assertEqual(timer.segment_set.count(), 2)
        self.assertIsNone(timer.segment_set.last().stop_time)

class ViewTest(TestCase):

    def test_start_and_stop_timer(self):
        response = self.client.post(reverse('start_timer'))
        self.assertEqual(Timer.objects.count(), 1)
        response = self.client.post(reverse('stop_timer'))
        timer = Timer.objects.first()
        self.assertIsInstance(timer.duration(), timedelta)