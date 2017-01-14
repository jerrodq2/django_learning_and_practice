from django.conf.urls import url
from . import views

urlpatterns = [
    #MAIN ROUTES***********************************
    url(r'^$', views.index, name='index'),
    url(r'^admin$', views.admin, name='admin'),
    url(r'^destroy/(?P<id>\d+)$', views.destroy, name='destroy'),
    #NEW USER ROUTES***********************************
    url(r'^new$', views.new, name='new'),
    url(r'^create$', views.create, name='create'),
    #EDIT USER ROUTES***********************************
    url(r'^edit$', views.edit, name='edit'),
    url(r'^edit/info$', views.edit_info, name='edit_info'),
    url(r'^edit/password$', views.edit_password, name='edit_password'),
    url(r'^edit/description$', views.edit_description, name='edit_description'),
    #ADMIN EDIT USER ROUTES***********************************
    url(r'^edit/(?P<id>\d+)$', views.admin_edit, name='admin_edit'),
    url(r'^edit/info/(?P<id>\d+)$', views.admin_edit_info, name='admin_edit_info'),
    url(r'^edit/(?P<id>\d+)/password$', views.admin_edit_password, name='admin_edit_password'),

    #SHOW AND MESSAGE ROUTES***********************************
    url(r'^show/(?P<id>\d+)$', views.show, name='show'),
    url(r'^message/create/(?P<id>\d+)$', views.message, name='message'),
    url(r'^comment/create/(?P<uid>\d+)/(?P<mid>\d+)$', views.comment, name='comment'),

]
