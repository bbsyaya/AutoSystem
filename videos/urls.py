# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url

__author__ = 'GoTop'


from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/video/search?q=gta&max_results=10
    url(r'search/(?P<q>\w+)/(?P<max_results>\d+)$', views.search_view, name='search'),
    #url(r'search$', views.search_view, name='search'),
]