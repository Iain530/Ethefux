from django.conf.urls import url
from registration import views
import os

urlpatterns = [
    url(r'login/$', views.user_login, name="user_login"),
    url(r'register/$', views.user_register, name="user_register"),
    url(r'logout/$', views.user_logout, name="user_logout"),
    url(r'update/$', views.user_update, name="user_update"),
]
