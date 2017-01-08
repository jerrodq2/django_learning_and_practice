from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^course$', views.create, name='create'),
    url(r'^delete/(?P<id>\d+)$', views.confirm, name='confirm'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy, name='destroy'),
    url(r'^comments/(?P<id>\d+)$', views.comments, name='comment'),
    url(r'^create/comment/(?P<id>\d+)$', views.new, name='new'),

]
