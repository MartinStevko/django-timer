
from django.conf.urls import url
from django_timer import views

urlpatterns = [
    url(r'^start/$', views.start_timer, name='start_timer'),
    url(r'^pause/$', views.pause_timer, name='pause_timer'),
    url(r'^resume/$', views.resume_timer, name='resume_timer'),
    url(r'^stop/$', views.stop_timer, name='stop_timer'),
]