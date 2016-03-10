# coding=utf-8
from __future__ import unicode_literals, absolute_import
import os

from celery import task

import django

from django.utils.text import slugify, get_valid_filename
from AutoSystem.settings.base import YOUTUBE_DOWNLOAD_DIR
from video.libs.subtitle import merge_subtitle, add_subtitle_to_video, \
    srt_to_ass, edit_two_lang_style
from video.models import Video

from video.libs.convert_subtitles import convert_file

__author__ = 'GoTop'

from pysrt import SubRipFile, SubRipTime

"""
合并两种不同言语的字幕
参考 https://github.com/byroot/pysrt/issues/15
https://github.com/byroot/pysrt/issues/17
"""


def merge_video_subtitle(video_id):
    """
    将video_id的中英字幕进行合并为srt格式的字幕
    :param video_id:
    :return:
    """
    video = Video.objects.get(pk=video_id)

    # Settings default values
    delta = SubRipTime(milliseconds=500)
    encoding = "utf_8"

    if (video.subtitle_cn != '') & (video.subtitle_en != ''):

        # convert_file(input_captions = video.subtitle_cn, output_writer)

        # vtt格式的字幕
        subs_cn_vtt = SubRipFile.open(video.subtitle_cn.path, encoding=encoding)
        subs_en_vtt = SubRipFile.open(video.subtitle_en.path, encoding=encoding)

        # 将vtt字幕转换为srt
        subs_cn_srt_filename = '%s-%s.cn.srt' % (
            get_valid_filename(video.title), video.video_id)
        subs_cn_srt = os.path.join(YOUTUBE_DOWNLOAD_DIR, subs_cn_srt_filename)
        subs_cn_srt_result = convert_file(input_captions=video.subtitle_cn.path,
                                          output_writer=subs_cn_srt)

        subs_en_srt_filename = '%s-%s.cn.srt' % (
            get_valid_filename(video.title), video.video_id)
        subs_en_srt = os.path.join(YOUTUBE_DOWNLOAD_DIR, subs_en_srt_filename)
        subs_en_srt_result = convert_file(input_captions=video.subtitle_en.path,
                                          output_writer=subs_en_srt)

        merge_subs = merge_subtitle(subs_cn_srt, subs_en_srt, delta)

        # 某些youtube视频的title有非ASCII的字符，或者/等不能出现在文件名中的字符
        # 所以使用django utils自带的get_valid_filename()转化一下
        # 注意:与youtube-dl自带的restrictfilenames获得的文件名不一样,
        # 也就是merge_subs_filename  与 subtitle_cn， subtitle_cn中名称可能会不一样
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


@task
def add_subtitle_to_video_process(video_id, sub_lang_type='zh-Hans'):
    """
    将video_id对应的视频的字幕，硬入到对应的视频中

    :param video_id:
    :param subtitle_type: (en,zh-Hans,zh-Hans_en)
    :return:
    """
    video = Video.objects.get(pk=video_id)

    if sub_lang_type == 'zh-Hans' and video.subtitle_cn.name:
        subtitle_file = video.subtitle_cn.path

        ass_filename = '%s-%s.zh-Hans.ass' % (
        get_valid_filename(video.title), video_id)

        ass_subs_dir = os.path.join(YOUTUBE_DOWNLOAD_DIR, ass_filename)

        subtitle_file = srt_to_ass(subtitle_file, ass_subs_dir)
        # youtube上的英文vtt字幕包含格式，导致转换成srt字幕再和中文srt字幕合并后有代码
        # 暂时不知道该如何处理，所以只合并中文字幕到视频
    # elif sub_lang_type == 'en' and video.subtitle_en.name:
    #     subtitle_file = video.subtitle_en.path
    elif sub_lang_type == 'zh-Hans_en' and video.subtitle_merge.name:
        subtitle_file = video.subtitle_merge.path
    else:
        # 如果获取不到subtitle_file，则返回False
        return False

    if (video.file.name):
        # 获取到文件名称
        file_basename = os.path.basename(video.file.path)
    else:
        return False

    # 将文件名称分割为名称和后缀
    file_basename_list = os.path.splitext(file_basename)
    subtitle_video = file_basename_list[0] + '.' + sub_lang_type + \
                     file_basename_list[1]

    # 加入字幕的视频文件保存到YOUTUBE_DOWNLOAD_DIR 目录下
    subtitle_video = os.path.join(YOUTUBE_DOWNLOAD_DIR, subtitle_video)

    result = add_subtitle_to_video(video.file.path, subtitle_file,
                                   subtitle_video, 'hard')
    if result == True and os.path.exists(subtitle_video):
        # 如何将字幕合并到视频成功，则保存视频文件地址到Video module中
        video.subtitle_video_file = subtitle_video
        video.save()
        return True
    else:
        print(result)
        return False


def srt_to_ass_process(video_id, srt_file_dir):
    """
    将中英字幕合并成的srt字幕文件转换为ass格式字幕文件

    :param video_id:
    :param srt_file_dir:
    :return:
    """
    video = Video.objects.get(video_id=video_id)
    ass_filename = '%s-%s.zh-Hans.en.ass' % (
        get_valid_filename(video.title), video_id)

    ass_subs_dir = os.path.join(YOUTUBE_DOWNLOAD_DIR, ass_filename)

    srt_to_ass(srt_file_dir, ass_subs_dir)

    # 如果成功生成srt_file_dir文件，则将字幕文件地址返回
    if os.path.isfile(ass_subs_dir):
        video.subtitle_merge = ass_subs_dir
        video.save(update_fields=['subtitle_merge', ])
        return ass_subs_dir
    else:
        return False


@task
def merge_sub_edit_style(video_id):
    """
    合并srt字幕，然后将srt字幕转换为ass格式，添加双语字幕式样，合并到视频中

    :param video_id:
    :return:
    """
    # 将中英vtt格式的字幕合并为srt格式的字幕
    merge_subtitle_result = merge_video_subtitle(video_id)
    if merge_subtitle_result:

        # 将合并的srt字幕转换为ass格式字幕
        ass_subs_dir = srt_to_ass_process(video_id, merge_subtitle_result)

        # 修改双语字幕的式样
        merge_sub_file = edit_two_lang_style(ass_subs_dir)
        if merge_sub_file:
            return merge_sub_file
