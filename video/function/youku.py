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


def youku_upload(youku_id):
    youku_access_token = youku_get_authenticate()

    youku = Youku.objects.get(pk=youku_id)

    video_file_path = youku.video.file
    service = YoukuUpload(CLIENT_ID, youku_access_token, video_file_path)

    # 上传的时候如果video.description为None，youku这个库会提示object of type 'NoneType' has no len()
    if youku.description is None:
        description = ''
    else:
        description = youku.description

    if youku.tags == '':
        # 如果未设置tags，则将tags设置为category，因为tags是必选参数，不能为空
        youku.tags = youku.category

    tags = youku.tags

    # 参数 http://cloud.youku.com/docs?id=110
    # tags：string 必选参数 视频标签，自定义标签不超过10个，单个标签最少2个字符，最多12个字符（6个汉字），多个标签之间用逗号(,)隔开
    # category：string 可选参数 视频分类，详细分类定义见 http://cloud.youku.com/docs?id=90
    video_info = {
        'title': youku.title,
        'category': youku.category,
        'tags': tags,
        'description': description
    }
    youku_video_id = service.upload(video_info)

    youku.youku_video_id = youku_video_id
    youku.save()
    return youku_video_id


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


def set_youku_playlist(youku_video_id):
    """
    根据youku的youkuplaylist属性，在优酷网上将youku对象添加到该playlist中

    一个视频可以加入多个playlist，所以在youku中设置playlist后，如果不执行del_videos_from_playlist操作，视频仍然属于该playlist
    :param youku_id:
    :return:
    """
    youku = Youku.objects.get(youku_video_id=youku_video_id)

    if hasattr(youku, 'video'):
        service = YoukuPlaylists(CLIENT_ID)
        youku_access_token = youku_get_authenticate()
        # http://doc.open.youku.com/?docid=377
        # 视频ID用逗号来分割,每个专辑最多200个视频，限制单次操作视频的最大个数，默认20
        # video_ids=850,860,870,880
        id = service.add_videos_to_playlist(access_token=youku_access_token, playlist_id=youku.youku_playlist.id,
                                            video_ids=youku_video_id)

        if id:
            return id
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
