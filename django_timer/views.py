
from django.http.response import HttpResponse

from django_timer.models import Entry

def start_timer(request):
    Entry.objects.create()
    return HttpResponse()

def stop_timer(request):
    entry = Entry.objects.last()
    entry.stop()
    return HttpResponse()