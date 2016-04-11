# coding=utf-8
from __future__ import unicode_literals, absolute_import

import logging

from celery import task
from celery_once import QueueOnce

from oauth2_authentication.function.youku import youku_get_authenticate
from AutoSystem.settings import YOUKU_CLIENT_ID
from video.libs.youku import YoukuUpload, YoukuVideos, YoukuPlaylists

CLIENT_ID = YOUKU_CLIENT_ID

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings")
django.setup()

from video.models import Youku, Video, YoukuPlaylist

__author__ = 'GoTop'


@task(base=QueueOnce)
def youku_upload(youku_id, max_retey=8):
    """
    将youku id的youku对象对应的合并有字幕的video视频的上传到优酷网

    :param youku_id:
    :return:
    """
    youku_access_token = youku_get_authenticate()

    youku = Youku.objects.get(pk=youku_id)

    # 如果没有在将字幕合并到视频中，则使用原版的视频
    if youku.video.subtitle_video_file == '' and youku.video.file.name:
        # 如果 subtitle_video_file 不存在
        video_file_path = youku.video.file.path
    elif youku.video.subtitle_video_file.name:
        # 如果 subtitle_video_file 存在
        video_file_path = youku.video.subtitle_video_file.path
    else:
        return False

    service = YoukuUpload(CLIENT_ID, youku_access_token, video_file_path)

    # 如果没有在vidoe对应的youku model中设置中文title，则使用video中的title
    if youku.title == '':
        title = youku.video.title
    else:
        title = youku.title

    # 上传的时候如果video.description为None，youku这个库会提示object of type 'NoneType' has
    # no len()
    if youku.description is None:
        description = ''
    else:
        description = youku.description

    if youku.tags == '':
        # 如果未设置tags，则将tags设置为category，因为tags是必选参数，不能为空
        if youku.category:
            youku.tags = youku.category
        else:
            youku.tags = youku.video.get_tags(10)

    # tags = youku.tags

    # 参数 http://cloud.youku.com/docs?id=110
    # tags：string 必选参数 视频标签，自定义标签不超过10个，单个标签最少2个字符，最多12个字符（6个汉字），多个标签之间用逗号(,)隔开
    # category：string 可选参数 视频分类，详细分类定义见 http://cloud.youku.com/docs?id=90
    video_info = {
        'title': title,
        'category': youku.category,
        'tags': youku.tags,
        'description': description
    }
    n = 0
    try:
        youku_video_id = service.upload(video_info)
    except:
        if n + 1 < max_retey:
            youku_video_id = service.upload(video_info)
        else:
            return False

    youku.youku_video_id = youku_video_id
    youku.save()

    logger = logging.getLogger(__name__)
    logger.info("上传视频到优酷，id为" + youku.video_id)

    return youku_video_id


def delete_youku_video(youku_video_id):
    """
    在优酷网上删除youku_video_id的视频,成功的话将数据库youku.youku_video_id清零
    :param youku_video_id:
    :return:
    """
    service = YoukuVideos(CLIENT_ID)
    youku_access_token = youku_get_authenticate()
    delete_youku_video_id = service.destroy_video(
        access_token=youku_access_token,
        video_id=youku_video_id)

    if delete_youku_video_id == youku_video_id:
        # 在优酷网上成功删除视频后，在本地将youku.youku_video_id清空
        youku = Youku.objects.get(youku_video_id=youku_video_id)
        youku.youku_video_id = ''
        youku.save()
    return delete_youku_video_id


def update_youku_online_info(youku_video_id):
    """
    将youku_video_id的本地youku对象的属性，在优酷上进行更新

    :param youku_video_id:
    :return:
    """
    youku = Youku.objects.get(youku_video_id=youku_video_id)

    service = YoukuVideos(CLIENT_ID)

    youku_access_token = youku_get_authenticate()

    updated_youku_video_id = service.update_video(
        access_token=youku_access_token, video_id=youku_video_id,
        title=youku.title,
        tags=youku.tags, category=youku.category, copyright_type=None,
        public_type=None, watch_password=None,
        description=youku.description, thumbnail_seq=None)
    return updated_youku_video_id


def set_youku_category_local(youku_id):
    """
    根据youku_id获取对应的video的channel的category，
    将它的youku_playlist_category属性的值设置给youku.category
    :param youku_id:
    :return:
    """
    youku = Youku.objects.get(pk=youku_id)
    youku.category = \
        youku.video.channel.category.get_youku_playlist_category_display()

    youku.save(update_fields=['category'])
    return youku


def set_youku_playlist_online(youku_video_id, playlist_id):
    """
    根据youku的youkuplaylist属性，在优酷网上将youku对象添加到该playlist中

    一个视频可以加入多个playlist，所以在youku中设置playlist后，如果不执行del_videos_from_playlist
    操作，视频仍然属于该playlist
    :param youku_id:
    :return:
    """

    service = YoukuPlaylists(CLIENT_ID)
    youku_access_token = youku_get_authenticate()
    # http://doc.open.youku.com/?docid=377
    # 视频ID用逗号来分割,每个专辑最多200个视频，限制单次操作视频的最大个数，默认20
    # video_ids=850,860,870,880
    id = service.add_videos_to_playlist(access_token=youku_access_token,
                                        playlist_id=playlist_id,
                                        video_ids=youku_video_id)

    if id:
        return id
    else:
        return False


def delete_video_from_playlist(youku_video_id, playlist_id):
    """
    在playlist_id的优酷playlist中删除youku_video_id视频
    :param youku_video_id:
    :param playlist_id:
    :return:
    """
    service = YoukuPlaylists(CLIENT_ID)
    youku_access_token = youku_get_authenticate()

    try:
        id = service.del_videos_from_playlist(access_token=youku_access_token,
                                              playlist_id=playlist_id,
                                              video_ids=youku_video_id)
    except:
        # 如果playlist_id中没有youku_video_id，会提示异常，忽略即可
        pass
        return False

    if id:
        return id
    else:
        return False


def get_youku_playlist():
    """
    获取认证用户的playlist
    :return:
    """
    service = YoukuPlaylists(CLIENT_ID)
    youku_access_token = youku_get_authenticate()
    # http://doc.open.youku.com/?docid=377
    # 视频ID用逗号来分割,每个专辑最多200个视频，限制单次操作视频的最大个数，默认20
    # video_ids=850,860,870,880
    playlist_json = service.find_playlists_by_me(
        access_token=youku_access_token,
        orderby='published', page=1, count=20)


if __name__ == '__main__':
    set_youku_category_local(youku_id=3)
