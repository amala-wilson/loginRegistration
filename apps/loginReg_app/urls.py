from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^pokes$', views.pokes),
    url(r'^poke/(?P<id>\d+)$', views.newPoke)
]
