#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/10/19 下午3:11
# @Author  : iteemo
# @File    : urls.py

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^$', views.index, name='index'),
    url('^login/', views.loginview, name='login'),
    # url('article/(2003)/$',article_detail),
    # url('article/([0-9]{4})/[0-9]{2}/([0-9]{2})/$',article_detail),
    # url('article/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',article_detail)
    url('article/(?P<year>[0-9]{4})/$', views.article_detail),
    # url('article/(\d+)/',article_detail)
    url('^index/', views.Indexview.as_view(), name="Indexview"),
    url('^user/', views.user, name="user"),
    url('^userview/', views.Userview2.as_view(), name="Userview")

]
