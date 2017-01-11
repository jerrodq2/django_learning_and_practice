from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^reg$', views.reg, name='reg'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^books$', views.books, name='books'),
    url(r'^books/add$', views.add, name='add'),
    url(r'^books/create$', views.create, name='create'),
    url(r'^books/review/(?P<id>\d+)$', views.review, name='review'),
    url(r'^books/destroy$', views.destroy, name='destroy'),
    url(r'^books/(?P<id>\d+)$', views.show, name='show'),
    url(r'^users/(?P<id>\d+)$', views.user, name='user'),
]
