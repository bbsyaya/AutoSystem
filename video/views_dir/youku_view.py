# coding=utf-8
from __future__ import unicode_literals

import time
from datetime import datetime

from django.shortcuts import render, render_to_response
from youku import YoukuVideos, YoukuUpload
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
    youku, created = Youku.objects.update_or_create(video_id=video_id,
                                defaults={'title': video_info['title'],
                                          'tags': video_info['tags'],
                                          'description': video_info['description'],
                                          'category': video_info['category'],
                                          'published': published}
                                )

    return render_to_response('result.html', {'dict_items': video_info})
