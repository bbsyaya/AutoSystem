# coding=utf-8
from __future__ import unicode_literals, absolute_import
import platform
import subprocess

import os.path

import sys
from celery import task
from pysrt import SubRipFile, SubRipItem, SubRipTime
# from pysubs2.ssafile import SSAFile
import pysubs2
import ass

from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
from video.libs.ffmpeg_runner import FFMPegRunner

__author__ = 'GoTop'


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
    """
    合并两种不同言语的字幕
    参考 https://github.com/byroot/pysrt/issues/15
    https://github.com/byroot/pysrt/issues/17
    :param sub_a:
    :param sub_b:
    :param delta:
    :return:
    """
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


@task
def add_subtitle_to_video(video_file, subtitle, output_video_file, mode='soft'):
    """
    将video_id对应的视频的字母，软写入到对应的视频中

    :param video_id:
    :return:
    """

    if platform.system() == "Windows":
        FFMPEG_BIN = "ffmpeg.exe"  # on Windows
    else:
        FFMPEG_BIN = "ffmpeg"  # on Linux ans Mac OS

    import subprocess
    # http://stackoverflow.com/questions/21363334/how-to-add-font-size-in
    # -subtitles-in-ffmpeg-video-filter
    soft_add_subtitle_command = [FFMPEG_BIN,
                                 '-i', video_file,
                                 '-i', subtitle,
                                 '-codec', 'copy',
                                 '-map', '0',
                                 '-map', '1',
                                 output_video_file]

    # ffmpeg -i input.mkv -vf ass=subtitles.ass output.mp4
    hard_add_subtitle_command = [FFMPEG_BIN,
                                 '-i', os.path.basename(video_file),
                                 '-vf',
                                 "ass=%s" % os.path.basename(subtitle),
                                 os.path.basename(output_video_file)]

    if mode == 'hard':
        command = hard_add_subtitle_command
    else:
        command = soft_add_subtitle_command

    # os.chdir(YOUTUBE_DOWNLOAD_DIR)

    # stderr can be STDOUT, which indicates that the stderr data from the child
    # process should be captured into the same file handle as for stdout.
    # process = subprocess.Popen(command,
    #                            cwd=YOUTUBE_DOWNLOAD_DIR,
    #                            stdout=subprocess.PIPE,
    #                            stderr=subprocess.STDOUT)


    runner = FFMPegRunner()

    def status_handler(old, new):
        print "From {0}% to {1}%".format(old, new)

    result = runner.run_session(command = command,
                                status_handler=status_handler)
    return result




    # 能执行命令，但是不显示所有过程
    # for line in iter(process.stdout.readline, b''):
    #     print '>>> {}'.format(line.rstrip())


def srt_to_ass(srt_file, ass_file):
    """
    使用ffmpeg将srt格式的字幕转化为ass格式的字幕

    :param srt_file:
    :param ass_file:
    :return:
    """
    if platform.system() == "Windows":
        FFMPEG_BIN = "ffmpeg.exe"  # on Windows
    else:
        FFMPEG_BIN = "ffmpeg"  # on Linux ans Mac OS

    if os.path.isfile(ass_file):
        os.remove(ass_file)

    command = [FFMPEG_BIN,
               '-i', srt_file, ass_file]
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT)
    stdout, stderr = process.communicate()

    if stderr:
        print(stderr)
        return False
    else:
        return ass_file


def edit_two_lang_style(subtitle_file):
    """
    为ass格式的双语字幕设置style
    :param subtitle_file:
    :return:
    """

    with open(subtitle_file, "r") as f:
        subtitle = ass.parse(f)

        print(subtitle.styles)

        # {\fn宋体\fs20\shad2\4a&H50&\3c&HFF8000&\4c&HFF8000&}
        # Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour,
        # OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut,
        # ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow,
        # Alignment, MarginL, MarginR, MarginV, Encoding
        # Style: Default,方正黑体_GBK,21,&H00FFFFFF,&HF0000000,&H006C3300,
        # &H00000000,-1,0,0,0,100,100,0,0,1,2,1,2,5,5,5,134
        subtitle.styles[0].fontname = '方正黑体_GBK'
        subtitle.styles[0].fontsize = 21
        subtitle.styles[0].primary_color = '&H00FFFFFF'
        subtitle.styles[0].secondary_color = '&HF0000000'
        subtitle.styles[0].outline_color = '&H006C3300'
        subtitle.styles[0].back_color = '&H00000000'
        subtitle.styles[0].bold = -1
        subtitle.styles[0].border_style = 1
        subtitle.styles[0].outline = 2
        subtitle.styles[0].shadow = 1
        subtitle.styles[0].alignment = 2

        for events in subtitle.events:
            utf8string = events.text.decode("utf-8")
            events.text = utf8string.replace(
                r'\N',
                r'\N{\fn方正综艺_GBK\fs14\b0\c&HFFFFFF&\3c&H2F2F2F&\4c&H000000&}'
            )

        with open(subtitle_file, "w") as f:
            subtitle.dump_file(f)

        if os.path.exists(subtitle_file):
            return subtitle_file

def edit_cn_ass_subtitle_style(subtitle_file):
    """
    为ass格式的中文字幕设置style
    :param subtitle_file:
    :return:
    """

    with open(subtitle_file, "r") as f:
        subtitle = ass.parse(f)

        print(subtitle.styles)

        subtitle.styles[0].fontname = '方正黑体_GBK'
        subtitle.styles[0].fontsize = 21
        subtitle.styles[0].primary_color = '&H00FFFFFF'
        subtitle.styles[0].secondary_color = '&HF0000000'
        subtitle.styles[0].outline_color = '&H006C3300'
        subtitle.styles[0].back_color = '&H00000000'
        subtitle.styles[0].bold = -1
        subtitle.styles[0].border_style = 1
        subtitle.styles[0].outline = 2
        subtitle.styles[0].shadow = 1
        subtitle.styles[0].alignment = 2

        with open(subtitle_file, "w") as f:
            subtitle.dump_file(f)

        if os.path.exists(subtitle_file):
            return subtitle_file