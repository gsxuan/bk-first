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
from get_capacity import views

urlpatterns = (
    url(r'^$', views.home),
    #下拉数据获取
    url(r'^get_app/$', views.get_app),
    # url(r'^get_ip_by_appid/$', views.get_ip_by_appid),
    # url(r'^get_task_list/$', views.get_task_list),

    # #执行作业，获取容量
    # url(r'^execcute_task/$', views.execcute_task),
    # url(r'^get_capacity/$', views.get_capacity),

    # #获取数据视图
    # url(r'^chartdata/$', views.get_capacity_chartdata),
)
