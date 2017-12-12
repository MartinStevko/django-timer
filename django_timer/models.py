
from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _

class TimerException(Exception):
    pass

class TimerQuerySet(models.QuerySet):

    def start_timer(self):
        timer = self.create()
        timer.segment_set.create()
        return timer

class Timer(models.Model):

    objects = TimerQuerySet.as_manager()

    def duration(self):
        return sum([segment.duration() for segment in self.segment_set.all()], timedelta())

    def stop(self):
        self.segment_set.last().stop()

    def pause(self):
        return self.stop()

    def resume(self):
        if not self.segment_set.last().stop_time:
            raise TimerException(_('Cannot resume, if timer is still running.'))
        self.segment_set.create()

class Segment(models.Model):

    timer = models.ForeignKey(to=Timer)

    start_time = models.DateTimeField(auto_now_add=True)
    stop_time = models.DateTimeField(null=True)

    def duration(self):
        if not self.stop_time:
            raise TimerException(_('Cannot calculate duration, if timer is still running.'))
        return self.stop_time - self.start_time

    def stop(self):
        if not self.stop_time:
            self.stop_time = now()
            self.save()
