# coding=utf-8
from __future__ import unicode_literals
from django.conf.urls import patterns, include, url
from video.views_dir import youtube_view, youtube_subscription_view, \
    youtube_channel_view, youtube_playlist_view, youku_view, \
    youku_playlist_view, subtitle_view, video

__author__ = 'GoTop'

from django.conf.urls import patterns, url
from . import views

urlpatterns = [
    ##########################################################################
    # YouTube
    ##########################################################################
    # http://127.0.0.1:8000/video/search?q=gta&max_results=10
    url(r'^search/(?P<q>\w+)/(?P<max_results>\d+)$', views.search_view,
        name='search'),

    ##########################################################################
    # YouTube 获取视频信息
    ##########################################################################

    # 获取认证用户的youtube首页显示的订阅频道的视频信息，保存到本地数据库
    # http://127.0.0.1:8000/video/get_subscription_update_video/50
    # 1 如果没登陆django admin就访问这个页面，会被转到
    # http://127.0.0.1:8000/accounts/login/?next=/oauth2/authenticate
    # 提示Page not found (404)
    # 2 如果没访问 127.0.0.1:8000/oauth2/authenticate 进行认证就直接访问该页面，
    # 会提示 int 错误
    url(r'^get_subscription_update_video/(?P<max_results>\d+)$',
        youtube_view.get_subscription_update_video_view,
        name='my_youtube_homepage'),

    ##########################################################################
    # YouTube 下载视频、字幕
    ##########################################################################
    # 一次获取max_results个保存在Video model中的youtube视频的时长，播放数等额外信息
    # http://127.0.0.1:8000/video/get_multi_youtube_video_info
    url(r'^get_multi_youtube_video_info$',
        youtube_view.get_multi_youtube_video_info_view,
        name='get_multi_youtube_video_info'),

    # 下载num个已对标题进行翻译的youtube视频
    # http://127.0.0.1:8000/video/download_youtube_video/1
    url(r'^download_multi_youtube_video/(?P<num>\d+)$',
        youtube_view.download_multi_youtube_video_view),

    # 下载单个youtube视频，并将下载后的视频文件的目录保存到Video.file
    # http://127.0.0.1:8000/video/download_single_youtube_video/_9coAtC2PZI
    # 因为youtube的video id 里可能含有 - 号，所以这样要用 . 来 代替 \w
    url(r'^download_single_youtube_video/(?P<video_id>.+)$',
        youtube_view.download_single_youtube_video_view,
        name='download_single_youtube_video'),

    # 自动下载num个设置了youku title属性的video视频到本地
    # http://127.0.0.1:8000/video/auto_youtube_download/1
    url(r'^auto_youtube_download/(?P<num>\d+)$',
        youtube_view.auto_youtube_download_view),

    # 下载video的中英字幕并保存到video model中
    # http://127.0.0.1:8000/video/download_upload_video/cJ5uaUTnMps
    url(r'^download_subtitle/(?P<video_id>.+)$',
        youtube_view.download_subtitle_view, name='download_subtitle'),

    ###########################################################################
    # YouTube Channel
    ###########################################################################

    # 根据channel_id,获取channel的信息，并保存到数据库中
    # http://127.0.0.1:8000/video/get_youtube_channel_info
    # /UCEQpJTOXGkvS1UQsdCm6lLA
    url(r'^get_youtube_channel_info/(?P<channel_id>.+)$',
        youtube_channel_view.get_youtube_channel_info_view,
        name='get_youtube_channel_info'),

    # 获取认证用户订阅的频道的信息
    # http://127.0.0.1:8000/video/get_my_subscription
    url(r'^get_my_subscription$',
        youtube_subscription_view.get_my_subscribe_channel_view,
        name='my_subscription'),

    # 获取认证用户的youtube首页显示的订阅频道信息,显示出来，但是不保存
    # http://127.0.0.1:8000/video/my_homepage_subscription/50
    url(r'^my_homepage_subscription/(?P<max_results>\d+)$',
        views.my_homepage_subscription_view,
        name='my_youtube_homepage'),

    # 获取认证用户的watchlater列表
    # http://127.0.0.1:8000/video/my_watchlater_lists/1
    url(r'^my_watchlater_lists/(?P<max_results>\d+)$',
        views.my_watchlater_lists_view,
        name='my_watchlater_lists'),

    ###########################################################################
    # YouTube Playlist
    ###########################################################################

    # 获取youtube channel的playlist信息，并保存
    url(r'^get_youtube_playlist_info/(?P<youtube_channel_id>.+)/('
        r'?P<max_results>\d+)$',
        youtube_playlist_view.get_youtube_playlist_info_view,
        name='get_youtube_playlist_info'),

    # 获取youtube_playlist_id的所有video的信息,并保存到数据库中
    url(r'^get_youtube_playlist_video_info/(?P<youtube_playlist_id>.+)/('
        r'?P<max_results>\d+)$',
        youtube_playlist_view.get_youtube_playlist_video_info_view,
        name='get_youtube_playlist_video_info'),

    # 下载is_download属性设置为true的youtubeplaylist里的视频信息并保存到数据库中
    # http://127.0.0.1:8000/video/auto_get_youtube_playlist_video_info
    url(r'^auto_get_youtube_playlist_video_info$',
        youtube_playlist_view.auto_get_youtube_playlist_video_info_view,
        name='auto_get_youtube_playlist_video_info'),

    ###########################################################################
    # 字幕
    ###########################################################################

    # 合并video_id视频的中、英vtt字幕为ass字幕
    # http://127.0.0.1:8000/video/merge_subtitle/_9coAtC2PZI
    url(r'^merge_subtitle/(?P<video_id>.+)/$',
        subtitle_view.merge_subtitle_view,
        name='merge_subtitle'),

    # 合并srt字幕，然后将srt字幕转换为ass格式，添加双语字幕式样，合并到视频中
    # http://127.0.0.1:8000/video/merge_sub_edit_style/_9coAtC2PZI
    url(r'^merge_sub_edit_style/(?P<video_id>.+)/$',
        subtitle_view.merge_sub_edit_style_view,
        name='merge_sub_edit_style'),

    # 将video_id对应的Video对象的subtitle_cn指向的中文vtt格式字幕，
    # 转化为ass格式，保存到subtitle_merge字段
    # 然后修改ass字幕的文字式样
    # http://127.0.0.1:8000/video/change_vtt_to_ass_and_edit_style/_9coAtC2PZI
    url(r'^change_vtt_to_ass_and_edit_style/(?P<video_id>.+)/$',
        subtitle_view.change_vtt_to_ass_and_edit_style_view,
        name='change_vtt_to_ass_and_edit_style'),

    # 将指定语言类型的字幕合并到video_id的视频中
    # http://127.0.0.1:8000/video/merge_subtitle_to_video/_9coAtC2PZI/soft/merge
    url(r'^merge_subtitle_to_video/(?P<video_id>.{11})/(?P<mode>.+)/('
        r'?P<sub_lang_type>(en|zh-Hans|merge))$',
        subtitle_view.merge_subtitle_to_video_view,
        name='merge_subtitle_to_video'),

    ########################################################################
    # 优酷
    #########################################################################
    # 将从youtube下载的视频上传到优酷
    # http://127.0.0.1:8000/video/youku_upload/1
    url(r'^youku_upload/(?P<youku_id>.+)/$', youku_view.youku_upload_view,
        name='youku_upload'),

    # 在优酷网上删除youku_video_id的视频,成功的话将数据库youku.youku_video_id清零
    # http://127.0.0.1:8000/video/youku_upload/1
    url(r'^delete_youku_video/(?P<youku_video_id>.+)/$',
        youku_view.delete_youku_video_view,
        name='delete_youku_video'),

    # 根据优酷的video id，获取优酷网上video视频的相关信息
    # http://127.0.0.1:8000/video/get_youku_video/XMTQyOTQ3NzgyOA==
    # 因为优酷的video id 里可能含有 = 号，所以这样要用 . 来 代替 \w
    url(r'^get_youku_video_info/(?P<video_id>.+)$',
        youku_view.get_youku_video_info_view, name='get_youku_video_info'),

    # 获取youku认证账号的专辑playlist信息并保存到youku playlist数据库中
    # http://127.0.0.1:8000/video/get_my_playlists
    url(r'^get_my_playlists$', youku_playlist_view.get_my_playlists_view),

    # 根据youku的youku playlist属性，在优酷网上将youku对象添加到该playlist中
    # http://127.0.0.1:8000/video/set_youku_playlist/XMTQyOTQ3NzgyOA==
    url(r'^set_youku_playlist/(?P<youku_video_id>.+)$',
        youku_playlist_view.set_youku_playlist_view),

    # http://127.0.0.1:8000/video/update_youku_info/
    url(r'^update_youku_online_info/(?P<youku_video_id>.+)$',
        youku_view.update_youku_online_info_view,
        name='update_youku_online_info'),

    # http://127.0.0.1:8000/video/update_youku_info/
    #在playlist_config表中，根据video_id视频所属的youtube playlist对应的youku playlist
    #设置该视频在优酷上的playlist
    url(r'^set_youku_playlist_online_from_config_playlist/(?P<video_id>.+)$',
        youku_playlist_view.set_youku_playlist_online_from_config_playlist_view,
        name='set_youku_playlist_online_from_config_playlist'),

    # http://127.0.0.1:8000/video/auto_set_youku_category
    url(r'^auto_set_youku_category', youku_view.auto_set_youku_category_view),

    # http://127.0.0.1:8000/video/auto_youku_upload/1
    url(r'^auto_youku_upload/(?P<num>\d+)$', youku_view.auto_youku_upload_view),

    #########################################################################
    # 综合操作
    #########################################################################
    # 查找对应video的subtitle_video_file不是null（已经下载到本地,并且已经合并了字幕）,
    # youku_video_id为''(还没上传到优酷)
    # title和category的youku model
    # 将其上传到优酷网上
    # http://127.0.0.1:8000/video/auto_youku_upload/1
    url(r'^auto_youku_upload/(?P<num>\d+)$', youku_view.auto_youku_upload_view),

    # 下载video_id为 video_id 的youtube视频和中英字幕，合并字幕到视频，设置优酷目录，然后上传到优酷
    # http://127.0.0.1:8000/video/download_upload_video/cJ5uaUTnMps
    url(r'^download_upload_video/(?P<video_id>.+)$',
        video.download_upload_video_view, name='download_upload_video'),

    # 下载config model中设置好的youtube playlist中的num个视频，并上传到优酷，设置其playlist
    # http://127.0.0.1:8000/video/download_upload_playlist_video/1
    url(r'^download_playlist_video/(?P<num>\d+)$',
        video.download_playlist_video_view,
        name='download_upload_video'),

]
