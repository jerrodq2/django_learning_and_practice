from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^books$', views.books, name='books'),
    url(r'^author/(?P<id>\d+)$', views.author, name='author'),
    url(r'^books/add$', views.add_book, name='add_book'),
    url(r'^books/create$', views.create_book, name='create_book'),
    url(r'^books/(?P<id>\d+)/reviews/create$', views.create_review, name='create_review'),
    url(r'^reviews/(?P<book_id>\d+)/(?P<review_id>\d+)/destroy$', views.destroy_review, name='destroy_review'),
    url(r'^book/(?P<id>\d+)$', views.show_book, name='show_book'),
    url(r'^user/(?P<id>\d+)$', views.show_user, name='show_user'),

]
