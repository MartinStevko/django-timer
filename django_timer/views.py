
from django.http.response import HttpResponse

from django_timer.models import Timer

def start_timer(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    Timer.objects.start(user=user)
    return HttpResponse()

def pause_timer(request):
    timer = Timer.objects.last()
    timer.pause()
    return HttpResponse()

def resume_timer(request):
    timer = Timer.objects.last()
    timer.resume()
    return HttpResponse()

def stop_timer(request):
    timer = Timer.objects.last()
    timer.stop()
    return HttpResponse()