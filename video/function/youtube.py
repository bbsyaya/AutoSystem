# coding=utf-8
from __future__ import unicode_literals
from video.models import Video

__author__ = 'GoTop'

import youtube_upload, pafy

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
        print('Done downloading, now converting ...')


def get_translate_title_video(num):
    tran_video_list = Video.objects.filter(title_cn__isnull=True).order_by('publishedAt', 'title')[:num]


def download_youtube_video_main(num):
    """
    下载num个已对标题进行翻译的youtube视频
    :return:
    """
    tran_video_list = Video.objects.filter(title_cn__isnull=False).order_by('publishedAt', 'title')[:num]

    for idx, video in enumerate(tran_video_list):
        # 代码参考 https://github.com/rg3/youtube-dl/blob/master/README.md#embedding-youtube-dl
        # 参数 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L121-L269
        # ydl_opts = {
        #     'format': 'bestaudio/best',
        #     'postprocessors': [{'key': 'FFmpegExtractAudio',
        #                         'preferredcodec': 'mp3',
        #                         'preferredquality': '192',
        #                        }],
        #     'logger': MyLogger(),
        #     'progress_hooks': [my_hook],
        # }

        ydl_opts = {
            'verbose': True,
            'format': 'bestvideo+bestaudio',  # choice of quality
            'outtmpl': 'example.%(ext)s',  # name the location
            'noplaylist': True,  # only download single song, not playlist
            'postprocessors': [{
                                   'key': 'FFmpegExtractAudio',
                                   'preferredcodec': 'mp3',
                               }],
            'prefer_ffmpeg' : True,
            'ffmpeg_location': "E:\\Program Files\\ffmpeg\\bin"


        }

        # 参考 http://willdrevo.com/downloading-youtube-and-soundcloud-audio-with-python-and-pandas/
        # 支持参数列表 https://github.com/rg3/youtube-dl/blob/master/youtube_dl/options.py
        options = {
            'format': '160+250',  # choice of quality
            # 'extractaudio': True,  # only keep the audio
            #'audioformat': "mp3",  # convert to mp3
            'outtmpl': 'E:\%(title)s-%(id)s.%(ext)s',  # name the file the ID of the video
            'noplaylist': True,  # only download single song, not playlist
            'subtitleslangs': ['zh-Hans','en'],#要写成list的形式
            'writeautomaticsub': True,
            'merge_output_format': 'mkv',
            'embedsubtitles': True,
        }

        with youtube_dl.YoutubeDL(options) as ydl:
            # youtube_url = video.youtube_url
            # 用设置成list的形式
            ydl.download([video.youtube_url])

        # 控制for循环的次数，从而控制下载的视频数
        # 参考 http://stackoverflow.com/questions/3162271/get-loop-count-inside-a-python-for-loop
        if idx > num:
            break


def list_streams(youtube):
    print "Live streams:"

    list_streams_request = youtube.liveStreams().list(
        part="id,snippet",
        mine=True,
        maxResults=50
    )

    while list_streams_request:
        list_streams_response = list_streams_request.execute()

        for stream in list_streams_response.get("items", []):
            print "%s (%s)" % (stream["snippet"]["title"], stream["id"])

        list_streams_request = youtube.liveStreams().list_next(
            list_streams_request, list_streams_response)