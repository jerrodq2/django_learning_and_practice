from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process/(?P<place>\w+)$', views.process),
    url(r'^reset$', views.reset)
]
