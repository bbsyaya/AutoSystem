# coding=utf-8
from __future__ import unicode_literals, absolute_import

import json

__author__ = 'GoTop'

from video.models import Video, Youku

from factory import DjangoModelFactory, lazy_attribute, SubFactory, Sequence
from faker import Factory
from video.models import Video

# faker要写在class的外面
faker = Factory.create()


class VideoFactory(DjangoModelFactory):  # factory boy knows this is for the
    # Product model
    class Meta:
        model = 'video.Video'
        django_get_or_create = ('video_id',)

    video_id = faker.word
    title = Sequence(lambda n: 'YouTube Video Title ' + str(n))


class YoukuFactory(DjangoModelFactory):  # factory boy knows this is for the
    # Product model
    class Meta:
        model = 'video.Youku'
        django_get_or_create = ('youku_video_id',)

    youku_video_id = faker.word
    title = Sequence(lambda n: 'Youku Video Title ' + str(n))
    tags = json.dumps(faker.words(4))
    video = SubFactory(VideoFactory)




    # youku = factory.SubFactory(YoukuFactory)
