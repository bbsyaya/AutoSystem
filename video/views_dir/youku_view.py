# coding=utf-8
from __future__ import unicode_literals
import time
from datetime import datetime
from django.shortcuts import render, render_to_response
from youku import YoukuVideos, YoukuUpload, YoukuPlaylists
from AutoSystem import settings
from oauth2_authentication.function.youku import youku_get_authenticate
from video.models import Video, Youku

CLIENT_ID = settings.YOUKU_CLIENT_ID


def youku_upload_view(request, video_id):
    youku_access_token = youku_get_authenticate()

    video = Video.objects.get(video_id=video_id)

    video_file_path = video.file
    service = YoukuUpload(CLIENT_ID, youku_access_token, video_file_path)

    # 上传的时候如果video.description为None，youku这个库会提示object of type 'NoneType' has no len()
    if video.description is None:
        video.description = ''

    if video.youku:
        video_info = {
            'title': video.title_cn,
            'tags': 'Google,IO',
            'description': video.description
        }

    # 参数 http://cloud.youku.com/docs?id=110
    # tags：string 必选参数 视频标签，自定义标签不超过10个，单个标签最少2个字符，最多12个字符（6个汉字），多个标签之间用逗号(,)隔开
    # category：string 可选参数 视频分类，详细分类定义见 http://cloud.youku.com/docs?id=90

    video_info = {
        'title': video.title_cn,
        'tags': 'Google,IO',
        'description': video.description
    }
    youku_video_id = service.upload(video_info)

    youku, created = Youku.objects.get_or_create(video_id=youku_video_id)

    video.youku = youku
    video.save()

    return render_to_response('result.html', {'text': '上传成功, 在优酷上的video id为 ' + youku_video_id})


def get_youku_video_info_view(request, video_id):
    """
    根据优酷的video id，获取视频的相关信息
    :param request:
    :param video_id:
    :return:
    """
    youku_service = YoukuVideos(CLIENT_ID)
    video_info = youku_service.find_video_by_id(video_id)

    published = datetime.strptime(video_info['published'], "%Y-%m-%d %H:%M:%S")
    youku, created = Youku.objects.update_or_create(youku_video_id=video_id,
                                                    defaults={'title': video_info['title'],
                                                              'tags': video_info['tags'],
                                                              'description': video_info['description'],
                                                              'category': video_info['category'],
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
    playlists_json = youku_service.find_playlists_by_me(youku_access_token)
    return render_to_response('result.html', {'text': playlists_json})
