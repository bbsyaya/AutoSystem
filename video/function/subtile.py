# coding=utf-8
from __future__ import unicode_literals

import os
import django

from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings")
django.setup()

from video.models import Video

__author__ = 'GoTop'

import pysrt
from pysrt import SubRipFile, SubRipItem, SubRipTime

"""
合并两种不同言语的字幕
参考 https://github.com/byroot/pysrt/issues/15
https://github.com/byroot/pysrt/issues/17

暂时没心情弄，有空再说
2015-12-27
"""

sub_en = "E:\Media\Video\YouTube\LG K10 and K7 hands-on-_9coAtC2PZI.en.srt"
sub_cn = "E:\Media\Video\YouTube\LG K10 and K7 hands-on-_9coAtC2PZI.zh-Hans.srt"

subs = pysrt.open(sub_en)

# Settings default values
delta = SubRipTime(milliseconds=500)
encoding = "utf_8"


def join_lines(txtsub1, txtsub2):
    if (len(txtsub1) > 0) & (len(txtsub2) > 0):
        return txtsub1 + '\n' + txtsub2
    else:
        return txtsub1 + txtsub2


def find_subtitle(subtitle, from_t, to_t, lo=0):
    i = lo
    while i < len(subtitle):
        if subtitle[i].start >= to_t:
            break

        if (subtitle[i].start <= from_t) & (to_t <= subtitle[i].end):
            return subtitle[i].text, i
        i += 1

    return "", i


def merge_subtitle(sub_a, sub_b, delta):
    out = SubRipFile()
    intervals = [item.start.ordinal for item in sub_a]
    intervals.extend([item.end.ordinal for item in sub_a])
    intervals.extend([item.start.ordinal for item in sub_b])
    intervals.extend([item.end.ordinal for item in sub_b])
    intervals.sort()

    j = k = 0
    for i in xrange(1, len(intervals)):
        start = SubRipTime.from_ordinal(intervals[i - 1])
        end = SubRipTime.from_ordinal(intervals[i])

        if (end - start) > delta:
            text_a, j = find_subtitle(sub_a, start, end, j)
            text_b, k = find_subtitle(sub_b, start, end, k)

            text = join_lines(text_a, text_b)
            if len(text) > 0:
                item = SubRipItem(0, start, end, text)
                out.append(item)

    out.clean_indexes()
    return out


def add_subtitle_to_video(video_id):
    # FFMPEG_BIN = "ffmpeg" # on Linux ans Mac OS
    FFMPEG_BIN = "ffmpeg.exe"  # on Windows

    video = Video.objects.get(pk=video_id)

    subtitle_video = os.path.join(YOUTUBE_DOWNLOAD_DIR, 'out.mkv')

    import subprocess
    command = [FFMPEG_BIN,
               '-i', video.file,
               '-i', video.subtitle_cn,
               '-codec', 'copy',
               '-map', '0',
               '-map', '1',
               subtitle_video]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()
    return stdout


def main():
    subs_a = SubRipFile.open(sub_cn, encoding=encoding)
    subs_b = SubRipFile.open(sub_en, encoding=encoding)
    out = merge_subtitle(subs_a, subs_b, delta)
    out.save('E:\Media\Video\YouTube\out.srt', encoding=encoding)
    # print(out)


if __name__ == '__main__':
    video_id = '_9coAtC2PZI'
    stdout = add_subtitle_to_video(video_id)
    print(stdout)
