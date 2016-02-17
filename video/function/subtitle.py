# coding=utf-8
from __future__ import unicode_literals, absolute_import
import os
import platform

import django

from django.utils.text import slugify, get_valid_filename
from AutoSystem.settings.base import YOUTUBE_DOWNLOAD_DIR
from video.libs.subtitle import merge_subtitle
from video.models import Video

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings.local")
django.setup()

__author__ = 'GoTop'

from pysrt import SubRipFile, SubRipTime

"""
合并两种不同言语的字幕
参考 https://github.com/byroot/pysrt/issues/15
https://github.com/byroot/pysrt/issues/17
"""


def merge_video_subtitle(video_id):
    """
    将video_id的中英字幕进行合并
    :param video_id:
    :return:
    """
    video = Video.objects.get(pk=video_id)

    # Settings default values
    delta = SubRipTime(milliseconds=500)
    encoding = "utf_8"

    if (video.subtitle_cn != '') & (video.subtitle_en != ''):
        subs_cn = SubRipFile.open(video.subtitle_cn.path, encoding=encoding)
        subs_en = SubRipFile.open(video.subtitle_en.path, encoding=encoding)
        merge_subs = merge_subtitle(subs_cn, subs_en, delta)

        # 某些youtube视频的title有非ASCII的字符，或者/等不能出现在文件名中的字符
        # 所以使用django utils自带的get_valid_filename()转化一下
        # 注意:与youtube-dl自带的restrictfilenames获得的文件名不一样
        # 标题中的 . 依然会保留
        merge_subs_filename = '%s-%s.zh-Hans.en.srt' % (
            get_valid_filename(video.title), video.video_id)

        merge_subs_dir = os.path.join(YOUTUBE_DOWNLOAD_DIR, merge_subs_filename)

        merge_subs.save(merge_subs_dir, encoding=encoding)

        video.subtitle_merge = merge_subs_dir
        video.save()
        return merge_subs_dir
    else:
        return False


def add_subtitle_to_video(video_file, subtitle, output_video_file):
    """
    将video_id对应的视频的字母，软写入到对应的视频中

    :param video_id:
    :return:
    """

    if platform.system() == "Windows":
        FFMPEG_BIN = "ffmpeg.exe"  # on Windows
    else:
        FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS


    import subprocess
    command = [FFMPEG_BIN,
               '-i', video_file,
               '-i', subtitle,
               '-codec', 'copy',
               '-map', '0',
               '-map', '1',
               output_video_file]
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    if stderr:
        return stderr
    else:
        return True


def add_subtitle_to_video_process(video_id, sub_lang_type='zh-Hans'):
    """
    将video_id对应的视频的字母，软写入到对应的视频中

    :param video_id:
    :param subtitle_type: (en,zh-Hans,zh-Hans_en)
    :return:
    """
    video = Video.objects.get(pk=video_id)

    if sub_lang_type == 'en':
        subtitle_file = video.subtitle_en.path
    elif sub_lang_type == 'zh-Hans':
        subtitle_file = video.subtitle_cn.path
    elif sub_lang_type == 'zh-Hans_en':
        subtitle_file = video.subtitle_merge.path

    # 获取到文件名称
    file_basename = os.path.basename(video.file.path)
    # 将文件名称分割为名称和后缀
    file_basename_list = os.path.splitext(file_basename)
    subtitle_video = file_basename_list[0] + '.' + sub_lang_type + \
                     file_basename_list[1]

    # 加入字幕的视频文件保存到YOUTUBE_DOWNLOAD_DIR 目录下
    subtitle_video = os.path.join(YOUTUBE_DOWNLOAD_DIR, subtitle_video)

    result = add_subtitle_to_video(video.file.path, subtitle_file,
                                   subtitle_video)
    if result == True:
        # 如何将字幕合并到视频成功，则保存视频文件地址到Video module中
        video.subtitle_video_file = subtitle_video
        video.save()
        return True
    else:
        print(result)
        return False


def main():
    # Settings default values
    delta = SubRipTime(milliseconds=500)
    encoding = "utf_8"

    sub_en = "E:\Media\Video\YouTube\LG K10 and K7 hands-on-_9coAtC2PZI.en.srt"
    sub_cn = "E:\Media\Video\YouTube\LG K10 and K7 " \
             "hands-on-_9coAtC2PZI.zh-Hans.srt"
    subs_a = SubRipFile.open(sub_cn, encoding=encoding)
    subs_b = SubRipFile.open(sub_en, encoding=encoding)
    out = merge_subtitle(subs_a, subs_b, delta)
    out.save('E:\Media\Video\YouTube\out.srt', encoding=encoding)
    # print(out)

