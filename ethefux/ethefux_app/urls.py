from django.conf.urls import url
from ethefux_app import views

app_name = 'ethefux_app'

urlpatterns = [
	url(r'^$', views.index, name='index'),
        url(r'^$', views.about, name='about'),
        
]
