# coding=utf-8
from __future__ import unicode_literals, absolute_import

import json
from random import randint

from factory.fuzzy import FuzzyChoice

__author__ = 'GoTop'

from video.models import Video, Youku

from factory import DjangoModelFactory, lazy_attribute, SubFactory, Sequence
from faker import Factory
from video.models import Video

# faker要写在class的外面
# fake-factory提供的fake对象
# http://fake-factory.readthedocs.org/en/stable/providers
faker = Factory.create()

YOUKU_CATEGORY = ["Tech", "Games"]


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = 'video.Category'
    youku_playlist_category = FuzzyChoice(YOUKU_CATEGORY)


class YT_channelFactory(DjangoModelFactory):
    class Meta:
        model = 'video.YT_channel'

    channel_id = faker.uri()
    title = faker.last_name_male()
    category = SubFactory(CategoryFactory)


class VideoFactory(DjangoModelFactory):  # factory boy knows this is for the
    # Product model
    class Meta:
        model = 'video.Video'
        django_get_or_create = ('video_id',)

    video_id = faker.word
    title = Sequence(lambda n: 'YouTube Video Title ' + str(n))
    channel = SubFactory(YT_channelFactory)


class YoukuFactory(DjangoModelFactory):  # factory boy knows this is for the
    # Product model
    class Meta:
        model = 'video.Youku'
        django_get_or_create = ('youku_video_id',)

    # youku_id = randint(1, 100)
    youku_video_id = faker.word
    title = Sequence(lambda n: 'Youku Video Title ' + str(n))
    tags = json.dumps(faker.words(4))
    video = SubFactory(VideoFactory)
