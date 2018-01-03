
import json

from datetime import timedelta, datetime
from time import sleep

from django.test import TestCase
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.template import Template, Context
from django.http import HttpResponseNotAllowed
from django.contrib.auth.models import User

from django_timer.models import Timer, Segment, TimerResumeException, TimerStartException

class ModelTest(TestCase):

    def test_start_timer_through_manager(self):
        timer = Timer.objects.start()
        self.assertEqual(timer.segment_set.count(), 1)
        self.assertIsInstance(timer.segment_set.first().start_time, datetime)

    def test_start_timer_through_model(self):
        timer = Timer.objects.create()
        self.assertEqual(timer.segment_set.count(), 0)
        timer.start()
        self.assertEqual(timer.segment_set.count(), 1)
        self.assertIsInstance(timer.segment_set.last().start_time, datetime)

        # Starting again raises Error
        with self.assertRaises(TimerStartException):
            timer.start()

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
        with self.assertRaises(TimerResumeException):
            timer.resume()
        self.assertEqual(timer.segment_set.count(), 2)
        self.assertIsNone(timer.segment_set.last().stop_time)
        timer.pause()
        timer.resume()
        self.assertEqual(timer.segment_set.count(), 3)

    def test_timer_stopped(self):
        timer = Timer.objects.start()
        timer.stop()
        with self.assertRaises(TimerResumeException):
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

    def test_status_flags(self):
        t = Timer.objects.start()
        self.assertEqual(t.status, 'running')

        t.pause()
        self.assertEqual(t.status, 'paused')

        t.resume()
        self.assertEqual(t.status, 'running')

        t.stop()
        self.assertEqual(t.status, 'stopped')

class ViewTest(TestCase):

    def test_start_pause_resume_and_stop_timer(self):

        timer = Timer.objects.create()
        self.client.post(reverse('start_timer', args=(timer.pk,)))
        self.client.post(reverse('pause_timer', args=(timer.pk,)))
        self.assertIsInstance(Timer.objects.first().segment_set.last().stop_time, datetime)
        self.client.post(reverse('resume_timer', args=(timer.pk,)))
        self.assertEqual(Timer.objects.first().segment_set.count(), 2)
        self.assertIsNone(Timer.objects.first().segment_set.last().stop_time)
        self.client.post(reverse('stop_timer', args=(timer.pk,)))
        self.assertEqual(Timer.objects.first().status, 'stopped')

    def test_timer_view_response(self):
        # TimerView returns a json response with the timer duration and status

        timer = Timer.objects.create()
        response = self.client.post(reverse('start_timer', args=(timer.pk,)))
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        self.assertEqual(content['status'], 'running')
        self.assertEqual(content['duration'], 0)

    def test_method_not_allowed(self):

        timer = Timer.objects.create()

        response = self.client.get(reverse('start_timer', args=(timer.pk,)))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('pause_timer', args=(timer.pk,)))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('resume_timer', args=(timer.pk,)))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse('stop_timer', args=(timer.pk,)))
        self.assertEqual(response.status_code, 405)

    def test_pause_and_resume_race_conditions(self):
        
        timer = Timer.objects.create()

        self.client.post(reverse('start_timer', args=(timer.pk,)))
        self.client.post(reverse('pause_timer', args=(timer.pk,)))
        self.client.post(reverse('resume_timer', args=(timer.pk,)))

        # Resuming a second time shouldn't raise
        self.client.post(reverse('resume_timer', args=(timer.pk,)))

        self.client.post(reverse('stop_timer', args=(timer.pk,)))
        # Resuming or pausing a stopped timer shouldn't raise
        self.client.post(reverse('pause_timer', args=(timer.pk,)))
        self.client.post(reverse('resume_timer', args=(timer.pk,)))

    def test_stop_if_timer_is_not_running(self):

        timer = Timer.objects.create()
        self.client.post(reverse('start_timer', args=(timer.pk,)))
        self.client.post(reverse('stop_timer', args=(timer.pk,)))
        # Stopping a second time shouldn't raise
        self.client.post(reverse('stop_timer', args=(timer.pk,)))

class TemplateTagsTest(TestCase):

    def test_render_timer(self):
        timer = Timer.objects.start()
        template = Template('{% load timer %}{% render_timer timer %}')
        context = Context({'timer': timer})
        html = template.render(context)
        self.assertIn('id="django-timer"', html)

    def test_hhmmss(self):
        duration = timedelta(hours=1, minutes=3, seconds=20.1)
        context = Context({'duration': duration})
        self.assertEqual(
            Template('{% load timer %}{{ duration.total_seconds | hhmmss }}').render(context),
            '1:03:20'
        )
        self.assertEqual(
            Template('{% load timer %}{{ duration | hhmmss }}').render(context),
            '1:03:20'
        )
        