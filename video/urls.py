# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url

from video.views_dir import youtube_view


__author__ = 'GoTop'

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    # http://127.0.0.1:8000/video/search?q=gta&max_results=10
    url(r'search/(?P<q>\w+)/(?P<max_results>\d+)$', views.search_view, name='search'),

    # http://127.0.0.1:8000/video/my_subscription
    url(r'my_subscription$', views.my_subscription_view, name='my_subscription'),

    # http://127.0.0.1:8000/video/my_homepage_subscription/50
    url(r'my_homepage_subscription/(?P<max_results>\d+)$', views.my_homepage_subscription_view,
        name='my_youtube_homepage'),

    # http://127.0.0.1:8000/video/my_watchlater_lists/1
    url(r'my_watchlater_lists/(?P<max_results>\d+)$', views.my_watchlater_lists_view,
        name='my_watchlater_lists'),


    # http://127.0.0.1:8000/video/get_subscription_update_video/50
    url(r'get_subscription_update_video/(?P<max_results>\d+)$', youtube_view.get_subscription_update_video_view,
        name='my_youtube_homepage'),

    # http://127.0.0.1:8000/video/download_youtube_video/1
    url(r'download_youtube_video/(?P<num>\d+)$', youtube_view.download_youtube_video_view),


]