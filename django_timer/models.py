
from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class TimerException(Exception):
    pass

class TimerQuerySet(models.QuerySet):

    def get_or_start(self, user=None):
        try:
            return self.get_for_user(user=user)
        except Timer.DoesNotExist:
            return self.start(user=user)

    def get_for_user(self, user=None):
        return self.get(stopped=False, user=user)

    def start(self, user=None):
        timer = self.create(user=user)
        timer.segment_set.create()
        return timer

class Timer(models.Model):

    user = models.ForeignKey(to=User, null=True)
    stopped = models.BooleanField(default=False)

    objects = TimerQuerySet.as_manager()

    def duration(self):
        return sum([segment.duration() for segment in self.segment_set.all()], timedelta())

    def stop(self):
        self.pause()
        self.stopped = True
        self.save()

    def pause(self):
        self.segment_set.last().stop()

    def resume(self):
        if self.stopped:
            raise TimerException(_('Timer has been stopped and cannot be resumed.'))
        if not self.segment_set.last().stop_time:
            raise TimerException(_('Cannot resume, if timer is still running.'))
        self.segment_set.create()

class Segment(models.Model):

    timer = models.ForeignKey(to=Timer)

    start_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(null=True)

    def duration(self):
        if not self.stop_time:
            return now() - self.start_time
        return self.stop_time - self.start_time

    def stop(self):
        if not self.stop_time:
            self.stop_time = now()
            self.save()
