# coding=utf-8
from __future__ import unicode_literals
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