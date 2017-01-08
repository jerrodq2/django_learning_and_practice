from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^course$', views.create),
    url(r'^delete/(?P<id>\d+)$', views.confirm),
    url(r'^destroy/(?P<id>\d+)$', views.destroy),
    url(r'^comments/(?P<id>\d+)$', views.comments),
    url(r'^create/comment/(?P<id>\d+)$', views.new),

]
