
from django.conf.urls import url
from django_timer import views

urlpatterns = [
    url(r'^start/$', views.start_timer, name='start_timer'),
    url(r'^stop/$', views.stop_timer, name='stop_timer'),
]