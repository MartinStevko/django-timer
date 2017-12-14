
from django.conf.urls import url, include
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from django_timer.models import Timer

class TimerView(DetailView):
    model = Timer
    context_object_name = 'timer'

class IndexView(ListView):
    model = Timer

def index(request):
    user = request.user if request.user.is_authenticated else None
    try:
        timer = Timer.objects.filter(user=user).last()
    except Timer.DoesNotExist:
        timer = None
    return render(request, 'tests/index.html', {'timer': timer})

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<pk>\d+)/$', TimerView.as_view(), name='detail'),
    url(r'', include('django_timer.urls')),
]