# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url

from video.views_dir import youtube_view, youtube_subscription_view, youku_view

__author__ = 'GoTop'

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    ###########
    # YouTube
    ###########
    # http://127.0.0.1:8000/video/search?q=gta&max_results=10
    url(r'search/(?P<q>\w+)/(?P<max_results>\d+)$', views.search_view, name='search'),

    #####################
    # YouTube 订阅链接
    #####################
    # http://127.0.0.1:8000/video/get_my_subscription
    url(r'get_my_subscription$', youtube_subscription_view.get_my_subscription_view, name='my_subscription'),

    # http://127.0.0.1:8000/video/my_homepage_subscription/50
    url(r'my_homepage_subscription/(?P<max_results>\d+)$', views.my_homepage_subscription_view,
        name='my_youtube_homepage'),

    # http://127.0.0.1:8000/video/my_watchlater_lists/1
    url(r'my_watchlater_lists/(?P<max_results>\d+)$', views.my_watchlater_lists_view,
        name='my_watchlater_lists'),

    # http://127.0.0.1:8000/video/get_subscription_update_video/50
    # 1 如果没登陆django admin就访问这个页面，会被转到 http://127.0.0.1:8000/accounts/login/?next=/oauth2/authenticate
    # 提示Page not found (404)
    # 2 如果没访问 127.0.0.1:8000/oauth2/authenticate 进行认真就直接访问该页面，会提示 int 错误
    url(r'get_subscription_update_video/(?P<max_results>\d+)$', youtube_view.get_subscription_update_video_view,
        name='my_youtube_homepage'),

    # 下载num个已对标题进行翻译的youtube视频
    # http://127.0.0.1:8000/video/download_youtube_video/1
    url(r'download_multi_youtube_video/(?P<num>\d+)$', youtube_view.download_multi_youtube_video_view),

    # http://127.0.0.1:8000/video/download_single_youtube_video/zmZfonO6PkI
    # 因为youtube的video id 里可能含有 - 号，所以这样要用 . 来 代替 \w
    url(r'download_single_youtube_video/(?P<video_id>.+)$', youtube_view.download_single_youtube_video_view,
        name='download_single_youtube_video'),

    ###########
    # 优酷
    ###########
    # http://127.0.0.1:8000/video/youku_upload/z0zvQfLOcLM
    url(r'youku_upload/(?P<video_id>.+)/$', youku_view.youku_upload_view, name='youku_upload'),

    # http://127.0.0.1:8000/video/get_youku_video/XMTQyOTQ3NzgyOA==
    # 因为优酷的video id 里可能含有 = 号，所以这样要用 . 来 代替 \w
    url(r'get_youku_video_info/(?P<video_id>.+)$', youku_view.get_youku_video_info_view, name='get_youku_video_info'),

    # http://127.0.0.1:8000/video/get_my_playlists
    url(r'get_my_playlists$', youku_view.get_my_playlists_view, name='youku_upload'),


]
