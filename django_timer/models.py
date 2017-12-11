
from django.db import models
from django.utils.timezone import now

class Entry(models.Model):

    start_time = models.DateTimeField(auto_now=True)
    stop_time = models.DateTimeField(null=True)

    def duration(self):
        return self.stop_time - self.start_time

    def stop(self):
        self.stop_time = now()
        return self.save()