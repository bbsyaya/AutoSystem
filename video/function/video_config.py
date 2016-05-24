# coding=utf-8
from __future__ import unicode_literals, absolute_import

from video.function.youtube_download import download_single_youtube_video_main
from video.models import VideoConfig

__author__ = 'GoTop'


def download_video(num):
    """
    下载config model中设置好的youtube channel中的视频
    :param num:
    :return:
    """
    config = VideoConfig.objects.filter(is_enable = True)
    #如果设置了需要下载的youtube playlist，则获取该playlist下的video id，下载
    if config.youtube_playlist:

        download_single_youtube_video_main(video_id, max_retey=5, file_extend=
'mp4')
    if config.youtube_channel:
        pass




