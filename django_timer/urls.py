
from django.conf.urls import url
from django_timer import views

urlpatterns = [
    url(r'^start/$', views.Start.as_view(), name='start_timer'),
    url(r'^pause/$', views.Pause.as_view(), name='pause_timer'),
    url(r'^resume/$', views.Resume.as_view(), name='resume_timer'),
    url(r'^stop/$', views.Stop.as_view(), name='stop_timer'),
]