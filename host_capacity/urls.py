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

from host_capacity import views
from host_capacity import host_capacity_apis

urlpatterns = (
    url(r'^$', views.show_host_capacity_usage),
    url(r'^get_chart_data/$', views.get_host_capacity_usage_data),
    url(r'^disk_api_check/$', views.show_disk_api_page),
    url(r'^update_mounted_list/$', views.update_mounted_list),
    url(r'^get_disk_capacity/$', views.get_disk_capacity_data),
    url(r'^check_history/$', views.get_check_history),
)
