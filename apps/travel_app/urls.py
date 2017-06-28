from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
    url(r'^travels$', views.travels, name='travels'),
    url(r'^join/(?P<destination_id>\d+)$', views.join, name='join'),
    url(r'^travels/destination/(?P<destination_id>\d+)$', views.destination, name='destination'),
    url(r'^travels/add$', views.add, name='add'),
    url(r'^post_trip$', views.post_trip, name='post_trip'),
    url(r'^logout$', views.logout, name='logout')
]
