"""forDance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from freeStyle import views as dance_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', dance_views.toDance),
    url(r'^toDance/', dance_views.toDance),
    url(r'^getDance/', dance_views.getDance),
    url(r'^success/', dance_views.successPage),
    url(r'^record/', dance_views.recordPage),
    url(r'^upload/', dance_views.uploadImg),

    url(r'^upload', dance_views.uploadImg),
    url(r'^show', dance_views.showImg),
    url(r'^router$', dance_views.routerAlex),
    url(r'^router_alex$', dance_views.routerAlex)

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
