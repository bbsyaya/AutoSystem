# coding=utf-8
from __future__ import unicode_literals, absolute_import
import json
import time
from datetime import datetime
from django.db.models import Q
from django.shortcuts import render, render_to_response
from youku import YoukuVideos, YoukuUpload, YoukuPlaylists
from AutoSystem.settings.base import YOUKU_CLIENT_ID
from oauth2_authentication.function.youku import youku_get_authenticate
from video.function.youku import set_youku_category, youku_upload, \
    update_youku_online_info, set_youku_playlist, \
    delete_youku_video
from video.models import Video, Youku, YoukuPlaylist

CLIENT_ID = YOUKU_CLIENT_ID


def youku_upload_view(request, youku_id):
    """
    将youtube上下载的视频上传到优酷
    :param request:
    :param video_id: YouTube的video_id
    :return:
    """
    youku_video_id = youku_upload(youku_id)
    return render_to_response('result.html', {
        'text': '上传成功, 在优酷上的video id为 ' + youku_video_id})


def set_youku_playlist_view(request, youku_id):
    youku = Youku.objects.get(pk=youku_id)
    result = set_youku_playlist(youku.youku_video_id, youku.youku_playlist_id)
    return render_to_response('result.html',
                              {'text': '更新playlist成功, youku_id为 ' + youku_id})


def update_youku_online_info_view(request, youku_video_id):
    updated_youku_video_id = update_youku_online_info(youku_video_id)
    updated_youku_playlist_video_id = set_youku_playlist(youku_video_id)

    return render_to_response('result.html', {
        'text': '更新成功, 在优酷上的video id为 ' + updated_youku_video_id})


def get_youku_video_info_view(request, video_id):
    """
    根据优酷的video id，获取优酷网上video视频的相关信息
    :param request:
    :param video_id:
    :return:
    """
    youku_service = YoukuVideos(CLIENT_ID)
    video_info = youku_service.find_video_by_id(video_id)

    published = datetime.strptime(video_info['published'], "%Y-%m-%d %H:%M:%S")
    youku, created = Youku.objects.update_or_create(youku_video_id=video_id,
                                                    defaults={
                                                        'title': video_info[
                                                            'title'],
                                                        'tags': video_info[
                                                            'tags'],
                                                        'description':
                                                            video_info[
                                                                'description'],
                                                        'category': video_info[
                                                            'category'],
                                                        'published': published}
                                                    )

    return render_to_response('result.html', {'dict_items': video_info})


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
    return render_to_response('result.html', {'dict_in_list': playlists_dict})


def auto_set_youku_category_view(request):
    '''
    查找youku model中所有填写了title但是没有设置category的视频
    根据youku模块中的对应的youtube模块，查找其channel，再获取channel的category，
    根据category模块中设置的对应优酷categroy，设置youku模块中的category
    :param request:
    :return:
    '''
    youku_list = Youku.objects.filter(title__isnull=False).filter(
        category__isnull=True)

    youku_setted_list = []
    for youku in youku_list:
        youku_setted = set_youku_category(youku.id)
        youku_setted_list.append(youku_setted.title)

    return render_to_response('result.html', {'list': youku_setted_list})


def auto_youku_upload_view(request, num):
    """
    查找对应video的subtitle_video_file不是null（已经下载到本地,并且已经合并了字幕）, youku_video_id为''(还没上传到优酷)
    title和category的youku model
    将其上传到优酷网上
    :param request:
    :return:
    """
    youku_list = Youku.objects.filter(~Q(video__subtitle_video_file="")).filter(
        youku_video_id='').filter(
        ~Q(title='')).filter(
        ~Q(category=''))[:num]
    youku_uploaded_list = []
    for youku in youku_list:
        youku_uploaded = youku_upload(youku.id)
        youku_uploaded_list.append(youku_uploaded.title)

    return render_to_response('result.html', {'list': youku_uploaded_list})


def delete_youku_video_view(request, youku_video_id):
    """
    在优酷网上删除youku_video_id的视频,成功的话将数据库youku.youku_video_id清零
    :param request:
    :param youku_video_id:
    :return:
    """
    delete_youku_video_id = delete_youku_video(youku_video_id)
    return render_to_response('result.html', {'text': delete_youku_video_id +
                                                      '优酷视频已成功删除'})
