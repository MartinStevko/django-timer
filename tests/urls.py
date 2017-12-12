
from django.conf.urls import url, include
from django.shortcuts import render

from django_timer.models import Timer

def index(request):
    user = request.user if request.user.is_authenticated else None
    timer = Timer.objects.get_or_start(user=user)
    return render(request, 'tests/index.html', {'timer': timer})

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'', include('django_timer.urls')),
]