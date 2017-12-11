
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse

from django_timer.models import Entry

class TimerTest(TestCase):

    def test_start_and_stop_timer(self):
        response = self.client.post(reverse('start_timer'))
        self.assertEqual(Entry.objects.count(), 1)
        response = self.client.post(reverse('stop_timer'))
        entry = Entry.objects.first()
        self.assertIsInstance(entry.duration(), timedelta)