# coding=utf-8
from __future__ import unicode_literals, absolute_import
from celery import task
from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR, SETTING_FILE
from AutoSystem.settings import DEBUG
from video.models import Video, YT_channel
import youtube_dl
from video.function.file import search_keyword_in_file

def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

@task
def download_subtitle(video_id, subtitlesformat = 'vtt', max_retey=3):
    """
    下载video的中英字幕并保存到video model中

    :param video_id:
    subtitlesformat: vtt,srt, 参看youtube-dl中subtitlesformat
    :return:
    """
    subtitle_file_list = search_subtitles_file(video_id, subtitlesformat)
    if subtitle_file_list:
        return subtitle_file_list

    video = Video.objects.get(video_id=video_id)
    options = {
        'outtmpl': YOUTUBE_DOWNLOAD_DIR + '%(title)s-%(id)s.%(ext)s',
        # name the file the ID of the video
        'verbose': True,  # Print various debugging information
        'restrictfilenames': True,
        'subtitleslangs': ['zh-Hans' ],  # 要写成list的形式
        # 'convertsubtitles': 'srt',
        'subtitlesformat': subtitlesformat,
        'writeautomaticsub': True,  # 下载字幕，这里的字幕是youtube自动生成的CC字幕
        'skip_download': True,
        'progress_hooks': [my_hook],}

    # 如果是本地debug状态则使用代理
    if SETTING_FILE == 'local':
        options['socksproxy'] = '127.0.0.1:8115'

    with youtube_dl.YoutubeDL(options) as ydl:
        n = 0
        try:
            ydl.download([video.youtube_url])
        except:
            n = n + 1
            if n < max_retey:
                ydl.download([video.youtube_url])
            else:
                return False

    # 只适用于subtitlesformat设置为srt或ass的情况，设置为best则失效
    # 字幕名称格式 LG K10 and K7 hands-on-_9coAtC2PZI.en.srt
    return search_subtitles_file(video_id, subtitlesformat)


def search_subtitles_file(video_id, subtitle_format):
    """
    要自己查看下载目录下是否有相关video id的字幕文件
    入存在并将视频文件的地址保存到对应的字段
    :param video_id:
    :param subtitle_format:vtt, ass
    :return:
    """

    # 只能查找到一个这样的文件才对
    # if (filepath.__len__()) == 1:
    #     # 从list中把唯一的一个数据pop出来
    #     subtitle_filepath = filepath.pop()
    #     return subtitle_filepath
    # else:
    #     return False

    video = Video.objects.get(video_id=video_id)
    subtitle_en_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                  keyword=video_id +
                                                          ".en",
                                                  extend=subtitle_format)

    result = []
    if (subtitle_en_filepath.__len__()) == 1:
        # 从list中把唯一的一个数据pop出来
        video.subtitle_en = subtitle_en_filepath.pop()
        result.append(video.subtitle_en)

    subtitle_cn_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                  keyword=video_id
                                                          + ".zh-Hans",
                                                  extend=subtitle_format)
    if (subtitle_cn_filepath.__len__()) == 1:
        # 从list中把唯一的一个数据pop出来
        video.subtitle_cn = subtitle_cn_filepath.pop()
        result.append(video.subtitle_en)

    video.save(update_fields=["subtitle_en", "subtitle_cn"])

    if result == []:
        result = False
    return result
