from django.conf.urls import url
from ethefux_app import views

app_name = 'ethefux_app'

urlpatterns = [
	url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^dashboard/$', views.dashboard, name="dashboard"),
        url(r'^account/$', views.account, name="account"),
]
