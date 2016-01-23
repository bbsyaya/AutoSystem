# coding=utf-8
from __future__ import unicode_literals, absolute_import

from oauth2_authentication.function.youku import youku_get_authenticate

from AutoSystem import settings
from youku import YoukuUpload, YoukuVideos, YoukuPlaylists

CLIENT_ID = settings.YOUKU_CLIENT_ID

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings")
django.setup()

from video.models import Youku, Video

__author__ = 'GoTop'


def youku_upload(video_id):
    youku_access_token = youku_get_authenticate()

    video = Video.objects.get(video_id=video_id)

    video_file_path = video.file
    service = YoukuUpload(CLIENT_ID, youku_access_token, video_file_path)

    # 上传的时候如果video.description为None，youku这个库会提示object of type 'NoneType' has no len()
    if video.description is None:
        video.description = ''

    # 当video 实例设置了对应的youku实例，才上传数据
    if hasattr(video, 'youku'):
        # 参数 http://cloud.youku.com/docs?id=110
        # tags：string 必选参数 视频标签，自定义标签不超过10个，单个标签最少2个字符，最多12个字符（6个汉字），多个标签之间用逗号(,)隔开
        # category：string 可选参数 视频分类，详细分类定义见 http://cloud.youku.com/docs?id=90
        video_info = {
            'title': video.youku.title,
            'category': video.youku.category,
            'tags': video.youku.tags,
            'description': video.youku.description
        }

        youku_video_id = service.upload(video_info)
        return youku_video_id
    else:
        return False

        # todo 以下应该可以忽略
        # youku, created = Youku.objects.get_or_create(video_id=youku_video_id)
        #
        # video.youku = youku
        # video.save()


def update_youku_online_info(youku_video_id):
    """
    将youku_video_id的本地youku对象的属性，在优酷上进行更新

    :param youku_video_id:
    :return:
    """
    youku = Youku.objects.get(youku_video_id=youku_video_id)

    service = YoukuVideos(CLIENT_ID)

    youku_access_token = youku_get_authenticate()

    updated_youku_video_id = service.update_video(access_token=youku_access_token, video_id=youku_video_id,
                                                  title=youku.title,
                                                  tags=youku.tags, category=youku.category, copyright_type=None,
                                                  public_type=None, watch_password=None,
                                                  description=youku.description, thumbnail_seq=None)
    return updated_youku_video_id


def set_youku_category(youku_id):
    """
    根据youku_id获取对应的video的channel的category，将它的youku_playlist_category属性的值设置给youku.category
    :param youku_id:
    :return:
    """
    youku = Youku.objects.get(pk=youku_id)
    youku.category = youku.video.channel.category.youku_playlist_category
    youku.save()
    return youku


def set_youku_playlist(youku_id):
    """
    根据youku的youkuplaylist属性，在优酷网上将youku对象添加到该playlist中
    :param youku_id:
    :return:
    """
    youku = Youku.objects.get(pk=youku_id)

    if hasattr(youku, 'video'):
        service = YoukuPlaylists(CLIENT_ID)
        youku_access_token = youku_get_authenticate()
        # http://doc.open.youku.com/?docid=377
        # 视频ID用逗号来分割,每个专辑最多200个视频，限制单次操作视频的最大个数，默认20
        # video_ids=850,860,870,880
        id = service.add_videos_to_playlist(access_token=youku_access_token, playlist_id=youku.youku_playlist.id,
                                       video_ids=youku.video.id)

        if id:
            return True
    else:
        return False


def get_youku_playlist():
    service = YoukuPlaylists(CLIENT_ID)
    youku_access_token = youku_get_authenticate()
    # http://doc.open.youku.com/?docid=377
    # 视频ID用逗号来分割,每个专辑最多200个视频，限制单次操作视频的最大个数，默认20
    # video_ids=850,860,870,880
    playlist_json = service.find_playlists_by_me(access_token=youku_access_token,
                                                 orderby='published', page=1, count=20)


if __name__ == '__main__':
    set_youku_category(youku_id=3)
