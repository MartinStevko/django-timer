
from django.conf.urls import url
from django_timer import views

urlpatterns = [
    url(r'^start/$', views.Start.as_view(), name='start_timer'),
    url(r'^(?P<pk>\d+)/pause/$', views.Pause.as_view(), name='pause_timer'),
    url(r'^(?P<pk>\d+)/resume/$', views.Resume.as_view(), name='resume_timer'),
    url(r'^(?P<pk>\d+)/stop/$', views.Stop.as_view(), name='stop_timer'),
]