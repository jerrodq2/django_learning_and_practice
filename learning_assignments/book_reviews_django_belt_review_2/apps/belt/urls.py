from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^books$', views.books, name='books'),
    url(r'^books/add$', views.add, name='add'),
    url(r'^books/review$', views.add_review, name='add_review'),
    url(r'^review/destroy/(?P<rid>\d+)/(?P<bid>\d+)$', views.destroy, name='destroy'),
    url(r'^books/create/(?P<id>\d+)$', views.createReview, name='createReview'),
    url(r'^book/(?P<id>\d+)$', views.show, name='show'),
    url(r'^user/(?P<id>\d+)$', views.user, name='user'),
]
