# -*- coding: utf-8 -*-
"""testapp URL Configuration

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
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from home_application import views

urlpatterns = (
    url(r'^$', views.home),
    url(r'^hello2/$', views.hello2),
    url(r'^sayhello/$', views.say_hello),
    url(r'^hello3/$', views.hello3),
    url(r'^hostdata/$', views.host_data),
    url(r'^hello4/$', views.hello4),
    url(r'^get_dfusage/$', views.api_disk_usage),

    url(r'^hello5/$', views.hello5),
    url(r'^hello6/$', views.hello4),
)
