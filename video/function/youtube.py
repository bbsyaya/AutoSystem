# coding=utf-8
from __future__ import unicode_literals
import os
from AutoSystem import settings
from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
from video.function.subtitle import add_subtitle_to_video
from video.models import Video

__author__ = 'GoTop'

# import youtube_upload, pafy

import youtube_dl


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print(d)


def get_translate_title_video(num):
    tran_video_list = Video.objects.filter(title_cn__isnull=True).order_by('publishedAt', 'title')[:num]


def download_multi_youtube_video_main(num):
    """
    下载num个已对标题进行翻译的youtube视频
    :return:
    """
    # 选择出前num个已经翻译过标题的youtube视频
    tran_video_list = Video.objects.filter(title_cn__isnull=False).order_by('publishedAt', 'title')[:num]

    video_filepath_list = []
    for idx, video in enumerate(tran_video_list):
        video_filepath = download_single_youtube_video_main(video.video_id)
        video_filepath_list.append(video_filepath)

        # 将下载视频的目录保存到Video
        video.file = video_filepath
        video.save()
    return video_filepath_list

    # # 代码参考 https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
    # # 参数 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269
    # # 参考 http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas/
    # # 支持参数列表 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/options.py
    # options = {
    #     'format': '160+250',  # choice of quality
    #     # 'extractaudio': True,  # only keep the audio
    #     # 'audioformat': "mp3",  # convert to mp3
    #     'outtmpl': settings.YOUTUBE_DOWNLOAD_DIR + '\%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
    #     'noplaylist': True,  # only download single song, not playlist
    #     'verbose': True,
    #     'subtitleslangs': ['zh-Hans', 'en'],  # 要写成list的形式
    #     'writeautomaticsub': True,
    #     'embedsubtitles': True,
    #     'merge_output_format': 'mkv',
    #     'prefer_ffmpeg': True,
    #     'ffmpeg_location': "E:\\Program Files\\ffmpeg\\bin"
    #     # 'progress_hooks': [my_hook],
    # }
    #
    # video_filepath_list = []
    # for idx, video in enumerate(tran_video_list):
    #     with youtube_dl.YoutubeDL(options) as ydl:
    #         # youtube_url = video.youtube_url
    #         # 用设置成list的形式
    #         ydl.download([video.youtube_url])
    #
    #         # youtube-dl下载成功后并不会返回下载视频文件的信息
    #         # todo 所以要自己查看下载目录下是否有相关video id的视频，以此来判断是否下载成功
    #         # 并将视频文件的地址保存到对应的字段
    #         video_filepath = search_keyword_in_file(dir=settings.YOUTUBE_DOWNLOAD_DIR,
    #                                                 keyword=video.video_id,
    #                                                 extend=options.get('merge_output_format', None))
    #         if (video_filepath.__len__()) == 1:
    #             # 从list中把唯一的一个数据pop出来
    #             video_filepath = video_filepath.pop()
    #             video_filepath_list.append(video_filepath)
    #             video.file = video_filepath
    #             video.save()
    #     # 控制for循环的次数，从而控制下载的视频数
    #     # 参考 http://stackoverflow.com/questions/3162271/get-loop-count-inside-a-python-for-loop
    #     if idx > num:
    #         break
    #
    # # todo 返回成功下的的视频列表
    # return video_filepath_list


def download_single_youtube_video_main(video_id):
    """
    下载单个youtube视频，并将下载后的视频文件的目录保存到Video.file
    :param video_id:
    :return:
    """
    video = Video.objects.get(video_id=video_id)

    # 代码参考 https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
    # 参数 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269
    # 参考 http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas/
    # 支持参数列表 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/options.py
    options = {
        'format': '160+250',  # choice of quality
        # 'extractaudio': True,  # only keep the audio
        # 'audioformat': "mp3",  # convert to mp3
        'outtmpl': settings.YOUTUBE_DOWNLOAD_DIR + '\%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
        'noplaylist': True,  # only download single song, not playlist
        'verbose': True,
        'subtitleslangs': ['zh-Hans', 'en'],  # 要写成list的形式
        'writeautomaticsub': True,
        'embedsubtitles': True,
        'merge_output_format': 'mkv',
        'prefer_ffmpeg': True,
        'ffmpeg_location': "E:\\Program Files\\ffmpeg\\bin"
        # 'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        # youtube_url = video.youtube_url
        # 用设置成list的形式
        ydl.download([video.youtube_url])

        # youtube-dl下载成功后并不会返回下载视频文件的信息
        # todo 所以要自己查看下载目录下是否有相关video id的视频，以此来判断是否下载成功
        # 并将视频文件的地址保存到对应的字段
        video_filepath = search_keyword_in_file(dir=settings.YOUTUBE_DOWNLOAD_DIR,
                                                keyword=video.video_id,
                                                extend=options.get('merge_output_format', None))
        # 只能查找到一个这样的文件才对
        if (video_filepath.__len__()) == 1:
            # 从list中把唯一的一个数据pop出来
            video_filepath = video_filepath.pop()
            video.file = video_filepath
            video.save()
    return video_filepath


def search_keyword_in_file(dir, keyword, extend=None):
    """
    查找dir目录下，文件名中包含keyword，后缀为extend的文件
    :param dir:
    :param keyword:
    :param extend:
    :return:
    """
    file_list = []
    for root, subFolders, files in os.walk(dir):
        for file in files:
            if extend is not None:
                # 如果设置了要查找文件的extend
                # string.find() 返回的是查找到的文本的位置，查找不成功过则返回-1
                if file.find(keyword) != -1 and file.endswith(extend):
                    file_list.append(os.path.join(dir, file))
            else:
                # 如果没设置要查找的extend
                if file.find(keyword) != -1:
                    file_list.append(os.path.join(dir, file))

    return file_list





