# coding=utf-8
from __future__ import unicode_literals, absolute_import

import os

from video.libs.subtitle import convert_subtilte_format_wrapper
from video.models import Video

__author__ = 'GoTop'


def change_cn_vtt_to_ass(video_id):
    """
    将video_id的Video对象的中文vtt字幕，转化为ass字幕
    ass字幕的目录和名称与vtt字幕一样，仅后缀名不同
    :param video_id:
    :return:
    """
    video = Video.objects.get(video_id=video_id)

    if video:
        if video.subtitle_cn:
            ass_path = convert_subtilte_format_wrapper(video.subtitle_cn.path, 'ass')

            if ass_path:
                # 如果成功生成ass_path文件，则将字幕文件保存到video.subtitle_merge
                if os.path.isfile(ass_path):
                    video.subtitle_merge = ass_path
                    video.save(update_fields=['subtitle_merge', ])
                    return ass_path
                else:
                    return False
        else:
            return False
    else:
        return False
