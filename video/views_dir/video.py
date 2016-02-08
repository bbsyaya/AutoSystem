# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.shortcuts import render_to_response

from video.function.video import download_upload_video

__author__ = 'GoTop'


def download_upload_video_view(request, video_id):
    download_upload_video(video_id)
    return render_to_response('result.html',
                              {'text': '视频已下载并上传，优酷video id 为 ' + video_id}
                              )

