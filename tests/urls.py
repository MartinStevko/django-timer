
from django.conf.urls import url, include
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from django_timer.models import Timer

class IndexView(ListView):
    model = Timer

    def post(self, request):
        Timer.objects.create()
        return redirect('/')

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'', include('django_timer.urls')),
]