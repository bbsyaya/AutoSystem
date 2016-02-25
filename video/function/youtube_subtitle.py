# coding=utf-8
from __future__ import unicode_literals, absolute_import
from celery import task
from AutoSystem.settings.base import YOUTUBE_DOWNLOAD_DIR
from AutoSystem.settings.base import DEBUG
from video.models import Video, YT_channel
import youtube_dl
from video.function.file import search_keyword_in_file

@task
def download_subtitle(video_id):
    """
    下载video的中英字幕并保存到video model中

    :param video_id:
    :return:
    """
    video = Video.objects.get(video_id=video_id)
    options = {
        'outtmpl': YOUTUBE_DOWNLOAD_DIR + '\%(title)s-%(id)s.%(ext)s',
        # name the file the ID of the video
        'verbose': True,  # Print various debugging information
        'restrictfilenames': True,
        'subtitleslangs': ['en', 'zh-Hans'],  # 要写成list的形式
        # 'convertsubtitles': 'srt',
        'subtitlesformat': 'vtt',
        'writeautomaticsub': True,  # 下载字幕，这里的字幕是youtube自动生成的CC字幕
        'skip_download': True, }

    #如果是本地debug状态则使用代理
    if DEBUG == True:
        options['socksproxy'] = '127.0.0.1:8115'

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video.youtube_url])

        # 只适用于subtitlesformat设置为srt或ass的情况，设置为best则失效
        # 字幕名称格式 LG K10 and K7 hands-on-_9coAtC2PZI.en.srt
        subtitle_en_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                      keyword=video.video_id
                                                              + ".en",
                                                      extend=options.get(
                                                          'subtitlesformat',
                                                          None))

        result = []
        if (subtitle_en_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.subtitle_en = subtitle_en_filepath.pop()
            result.append(video.subtitle_en)

        subtitle_cn_filepath = search_keyword_in_file(dir=YOUTUBE_DOWNLOAD_DIR,
                                                      keyword=video.video_id
                                                              + ".zh-Hans",
                                                      extend=options.get(
                                                          'subtitlesformat',
                                                          None))
        if (subtitle_cn_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video.subtitle_cn = subtitle_cn_filepath.pop()
            result.append(video.subtitle_en)

        video.save()

    if result == []:
        result = False
    return result
