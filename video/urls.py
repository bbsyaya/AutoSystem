# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from video.views_dir import youtube_view, youtube_subscription_view, youku_view, \
    subtitle_view, video

__author__ = 'GoTop'

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    ############################################################################################
    # YouTube
    ############################################################################################
    # http://127.0.0.1:8000/video/search?q=gta&max_results=10
    url(r'search/(?P<q>\w+)/(?P<max_results>\d+)$', views.search_view,
        name='search'),

    #####################
    # YouTube 订阅链接
    #####################
    # http://127.0.0.1:8000/video/get_my_subscription
    url(r'get_my_subscription$',
        youtube_subscription_view.get_my_subscription_view,
        name='my_subscription'),

    # http://127.0.0.1:8000/video/my_homepage_subscription/50
    url(r'my_homepage_subscription/(?P<max_results>\d+)$',
        views.my_homepage_subscription_view,
        name='my_youtube_homepage'),

    # http://127.0.0.1:8000/video/my_watchlater_lists/1
    url(r'my_watchlater_lists/(?P<max_results>\d+)$',
        views.my_watchlater_lists_view,
        name='my_watchlater_lists'),

    # http://127.0.0.1:8000/video/get_subscription_update_video/50
    # 1 如果没登陆django admin就访问这个页面，会被转到 http://127.0.0.1:8000/accounts/login/?next=/oauth2/authenticate
    # 提示Page not found (404)
    # 2 如果没访问 127.0.0.1:8000/oauth2/authenticate 进行认真就直接访问该页面，会提示 int 错误
    url(r'get_subscription_update_video/(?P<max_results>\d+)$',
        youtube_view.get_subscription_update_video_view,
        name='my_youtube_homepage'),

    # 下载num个已对标题进行翻译的youtube视频
    # http://127.0.0.1:8000/video/download_youtube_video/1
    url(r'download_multi_youtube_video/(?P<num>\d+)$',
        youtube_view.download_multi_youtube_video_view),

    # http://127.0.0.1:8000/video/download_single_youtube_video/_9coAtC2PZI
    # 因为youtube的video id 里可能含有 - 号，所以这样要用 . 来 代替 \w
    url(r'download_single_youtube_video/(?P<video_id>.+)$',
        youtube_view.download_single_youtube_video_view,
        name='download_single_youtube_video'),

    # http://127.0.0.1:8000/video/auto_youtube_download/1
    url(r'auto_youtube_download/(?P<num>\d+)$',
        youtube_view.auto_youtube_download_view),

    # http://127.0.0.1:8000/video/download_upload_video/cJ5uaUTnMps
    url(r'download_upload_video/(?P<video_id>.+)$',
        video.download_upload_video_view, name='download_upload_video'),

    # http://127.0.0.1:8000/video/download_upload_video/cJ5uaUTnMps
    url(r'download_subtitle/(?P<video_id>.+)$',
        youtube_view.download_subtitle_view, name='download_subtitle'),

    ############################################################################################
    # 字幕
    ############################################################################################
    # http://127.0.0.1:8000/video/merge_subtitle/_9coAtC2PZI
    url(r'merge_subtitle/(?P<video_id>.+)/$', subtitle_view.merge_subtitle_view,
        name='merge_subtitle'),

    # http://127.0.0.1:8000/video/merge_subtitle_to_video/_9coAtC2PZI/zh-Hans_en
    url(
        r'^merge_subtitle_to_video/(?P<video_id>.{11})/(?P<sub_lang_type>(en|zh-Hans|zh-Hans_en))$',
        subtitle_view.merge_subtitle_to_video_view,
        name='merge_subtitle_to_video'),

    ############################################################################################
    # 优酷
    ############################################################################################
    # http://127.0.0.1:8000/video/youku_upload/1
    url(r'youku_upload/(?P<youku_id>.+)/$', youku_view.youku_upload_view,
        name='youku_upload'),

    # http://127.0.0.1:8000/video/youku_upload/1
    url(r'delete_youku_video/(?P<youku_video_id>.+)/$', youku_view.delete_youku_video_view,
        name='delete_youku_video'),


    # http://127.0.0.1:8000/video/get_youku_video/XMTQyOTQ3NzgyOA==
    # 因为优酷的video id 里可能含有 = 号，所以这样要用 . 来 代替 \w
    url(r'get_youku_video_info/(?P<video_id>.+)$',
        youku_view.get_youku_video_info_view, name='get_youku_video_info'),

    # http://127.0.0.1:8000/video/get_my_playlists
    url(r'get_my_playlists$', youku_view.get_my_playlists_view),

    # http://127.0.0.1:8000/video/set_youku_playlist/XMTQyOTQ3NzgyOA==
    url(r'set_youku_playlist/(?P<youku_video_id>.+)$',
        youku_view.set_youku_playlist_view),

    # http://127.0.0.1:8000/video/update_youku_info/
    url(r'update_youku_online_info/(?P<youku_video_id>.+)$',
        youku_view.update_youku_online_info_view,
        name='update_youku_online_info'),

    # http://127.0.0.1:8000/video/auto_set_youku_category
    url(r'auto_set_youku_category', youku_view.auto_set_youku_category_view),

    # http://127.0.0.1:8000/video/auto_youku_upload/1
    url(r'auto_youku_upload/(?P<num>\d+)$', youku_view.auto_youku_upload_view),

    ############################################################################################
    # 综合操作
    ############################################################################################
    # http://127.0.0.1:8000/video/auto_youku_upload/1
    url(r'auto_youku_upload/(?P<num>\d+)$', youku_view.auto_youku_upload_view),
]
