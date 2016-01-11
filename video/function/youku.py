# coding=utf-8
from __future__ import unicode_literals, absolute_import

from oauth2_authentication.function.youku import youku_get_authenticate
import os
import django
from AutoSystem import settings
from youku import YoukuUpload

CLIENT_ID = settings.YOUKU_CLIENT_ID

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
    pass


if __name__ == '__main__':
    set_youku_category(youku_id=3)
