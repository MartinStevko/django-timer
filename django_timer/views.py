
from django.http.response import HttpResponse

from django_timer.models import Timer

def start_timer(request):
    Timer.objects.start_timer()
    return HttpResponse()

def stop_timer(request):
    timer = Timer.objects.last()
    timer.stop()
    return HttpResponse()