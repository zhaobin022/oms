"""oms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from cmdb import urls as cmdb_urls
from codeonline import urls as codeonline_urls
from user_center import urls as user_center_urls
from monitor import urls as monitor_urls
from web_chat import urls as web_chat_urls
from saltapp import urls as saltapp_urls
import views
import settings


urlpatterns = [
    url(r'^$', views.index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cmdb/', include(cmdb_urls)),
    url(r'^codeonline/', include(codeonline_urls)),
    url(r'^user_center/', include(user_center_urls)),
    url(r'^monitor/', include(monitor_urls)),
    url(r'^web_chat/', include(web_chat_urls)),
    url(r'^saltapp/', include(saltapp_urls)),
]
