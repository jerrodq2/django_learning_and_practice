from django.conf.urls import url
from . import views

urlpatterns = [
    #MAIN ROUTES***********************************
    url(r'^$', views.index, name='index'),
    url(r'^signin$', views.signin, name='signin'),
    url(r'^login$', views.login, name='login'),
    url(r'^register$', views.register, name='register'),
    url(r'^register/create$', views.register_create, name='register_create'),
    url(r'^logout$', views.logout, name='logout'),

]
