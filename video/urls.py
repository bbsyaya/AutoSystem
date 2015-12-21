# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url

__author__ = 'GoTop'

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/video/search?q=gta&max_results=10
    url(r'search/(?P<q>\w+)/(?P<max_results>\d+)$', views.search_view, name='search'),

    # http://127.0.0.1:8000/video/my_subscription
    url(r'my_subscription$', views.my_subscription_view, name='my_subscription'),

    # http://127.0.0.1:8000/video/my_youtube_homepage/50
    url(r'my_youtube_homepage/(?P<max_results>\d+)$', views.my_youtube_homepage_view, name='my_youtube_homepage'),

    # http://127.0.0.1:8000/video/my_watchlater_lists/50
    url(r'my_watchlater_lists/(?P<max_results>\d+)$', views.my_watchlater_lists_view,
        name='my_youtube_homepage'),

]