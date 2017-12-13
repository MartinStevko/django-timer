
from django.conf.urls import url, include
from django.shortcuts import render

from django_timer.models import Timer

def index(request):
    user = request.user if request.user.is_authenticated else None
    try:
        timer = Timer.objects.filter(user=user).last()
    except Timer.DoesNotExist:
        timer = None
    return render(request, 'tests/index.html', {'timer': timer})

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'', include('django_timer.urls')),
]