# coding=utf-8
from __future__ import unicode_literals

from video.models import Youku

__author__ = 'GoTop'

def set_youku_category(youku_id):
    """
    根据youku_id获取对应的video的channel的category，将它的youku_playlist_category属性的值设置给youku.category
    :param youku_id:
    :return:
    """
    youku = Youku.objects.get(pk =youku_id )
    youku.category = youku.video.channel.category.youku_playlist_category
    youku.save()

def set_youku_playlist(youku_id):
    pass

