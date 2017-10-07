"""ethefux URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from ethefux_app import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('ethefux_app.urls')),
    url(r'^registration/', include('registration.urls', namespace="registration")),
    url(r'^login/$', views.user_login, name='login')

    # Error pages
    url(r'400', TemplateView.as_view(template_name='errors/400.html'), name="400"),
    url(r'403', TemplateView.as_view(template_name='errors/403.html'), name="403"),
    url(r'404', TemplateView.as_view(template_name='errors/404.html'), name="404"),
    url(r'500', TemplateView.as_view(template_name='errors/500.html'), name="500")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
