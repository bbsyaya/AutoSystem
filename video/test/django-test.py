# coding=utf-8
from __future__ import unicode_literals, absolute_import

from django.utils.text import get_valid_filename

from AutoSystem.settings import YOUTUBE_DOWNLOAD_DIR
from video.function.file import get_size, clean_media_root
from video.function.youku import set_youku_category
from video.libs.subtitle import srt_to_ass, edit_two_lang_style
from video.models import Video

__author__ = 'GoTop'

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AutoSystem.settings")
django.setup()

# get_video_info(video_id = 'QTCJJiZrNYo')

# clean_media_root(max_size=10 * 1024 * 1024, num=1)

# video = Video.objects.get(video_id='QTCJJiZrNYo')
#
# srt_file = video.subtitle_merge.path
# print srt_file
# ass_file = '%s-%s.zh-Hans.en.ass' % (
#     get_valid_filename(video.title), video.video_id)
# print ass_file
#
# merge_subs_dir = os.path.join(YOUTUBE_DOWNLOAD_DIR, ass_file)
# print merge_subs_dir
#
# srt_to_ass(srt_file, merge_subs_dir)
#
# edit_two_lang_style(merge_subs_dir)

video = Video.objects.get(video_id='pSahhWDQRW0')
set_youku_category(video.youku.id)
