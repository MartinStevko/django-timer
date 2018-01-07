
from datetime import timedelta

from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class TimerException(Exception):
    pass

class TimerStartException(TimerException):
    pass

class TimerResumeException(TimerException):
    pass

class TimerQuerySet(models.QuerySet):

    def start(self, user=None):
        timer = self.create(user=user)
        timer.start()
        return timer

class Timer(models.Model):

    STATUS = (
        ('running', _('running')),
        ('paused', _('paused')),
        ('stopped', _('stopped')),
    )

    user = models.ForeignKey(to=User, null=True)
    status = models.CharField(max_length=12, choices=STATUS)

    objects = TimerQuerySet.as_manager()

    def duration(self):
        return sum([segment.duration() for segment in self.segment_set.all()], timedelta())

    def start(self):
        if self.segment_set.count() > 0:
            raise TimerStartException(_('Timer has already been started.'))
        self.segment_set.create()
        self.status = 'running'
        self.save()

    def stop(self):
        self.pause()
        self.status = 'stopped'
        self.save()

    def pause(self):
        self.segment_set.last().stop()
        self.status = 'paused'
        self.save()

    def resume(self):
        if self.status == 'stopped':
            raise TimerResumeException(_('Timer has been stopped and cannot be resumed.'))
        if not self.segment_set.last().stop_time:
            raise TimerResumeException(_('Cannot resume, if timer is still running.'))
        self.segment_set.create()
        self.status = 'running'
        self.save()

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
