# coding=utf-8
from __future__ import unicode_literals, absolute_import
from django.shortcuts import render, render_to_response
from oauth2_authentication.function.youku import youku_get_authenticate
from video.function.youku_playlist import set_youku_playlist_online, \
    set_youku_playlist_online_from_playlist_config
from video.models import Youku, YoukuPlaylist
from video.libs.youku import YoukuVideos, YoukuUpload, YoukuPlaylists
from AutoSystem.settings import YOUKU_CLIENT_ID

CLIENT_ID = YOUKU_CLIENT_ID

__author__ = 'GoTop'


def set_youku_playlist_view(request, youku_id):
    """
    根据youku的youku playlist属性，在优酷网上将youku对象添加到该playlist中
    :param request:
    :param youku_id:
    :return:
    """
    youku = Youku.objects.get(pk=youku_id)
    result = set_youku_playlist_online(youku.youku_video_id,
                                       youku.youku_playlist_id)
    return render_to_response('result.html',
                              {'text': '更新playlist成功, youku_id为 ' + youku_id})


def set_youku_playlist_online_from_config_playlist_view(request, video_id):
    """
    在playlist_config表中，根据video_id视频所属的youtube playlist对应的youku playlist
    设置该视频在优酷上的playlist
    :param video_id:
    :return:
    """
    result = set_youku_playlist_online_from_playlist_config(video_id)
    if result:
        setted_playlist_id_list = result

    return render_to_response('result.html',
                              {'text': '更新video_id 为' + video_id +
                                       '的视频在优酷上的playlist成功, playlist_id为:',
                               'list': setted_playlist_id_list}
                              )


def get_my_playlists_view(request):
    """
    获取认证账号的专辑playlist
    :param request:
    :return:
    """
    youku_access_token = youku_get_authenticate()
    youku_service = YoukuPlaylists(CLIENT_ID)
    playlists_dict = youku_service.find_playlists_by_me(youku_access_token)
    for playlist in playlists_dict['playlists']:
        YoukuPlaylist.objects.update_or_create(id=playlist['id'],
                                               defaults={
                                                   'name': playlist['name'],
                                                   'duration': playlist[
                                                       'duration'],
                                                   'link': playlist['link'],
                                                   'play_link': playlist[
                                                       'play_link'],
                                                   'view_count': playlist[
                                                       'view_count'],
                                                   'video_count': playlist[
                                                       'video_count'], }
                                               )
    return render_to_response('result.html', {'text': "获取认证用户的Playlist信息成功",
                                              'dict_items': playlists_dict})
