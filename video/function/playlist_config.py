# coding=utf-8
from __future__ import unicode_literals, absolute_import
from video.models import PlaylistConfig, Video

__author__ = 'GoTop'


def get_youku_playlist_from_playlist_config(video_id):
    """
    根据视频video_id所属的youtube playlist，在PlaylistConfig 中查找其对应
    的youku playlist，可能是1-n个
    :param video_id:
    :return:PlaylistConfig对象
    """
    video = Video.objects.get(video_id=video_id)
    youtube_playlist = video.playlist
    playlist_config_list = PlaylistConfig.objects.filter(
        youtube_playlist=youtube_playlist)

    return playlist_config_list