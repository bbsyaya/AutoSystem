# coding=utf-8
from __future__ import unicode_literals, absolute_import

__author__ = 'GoTop'


from video.models import Video, Youku

import factory
from faker import Factory
from video.models import Video

class YoukuFactory(factory.Factory): # factory boy knows this is for the
    # Product model
    class Meta:
        model = 'video.Youku'
        django_get_or_create = ('youku_id',)
    title = factory.Sequence(lambda n: 'Youku Video Title ' + n)

    faker = Factory.create()
    tags = faker.words(4)
    video = factory.SubFactory(VideoFactory)

class VideoFactory(factory.Factory): # factory boy knows this is for the
    # Product model
    class Meta:
        model = 'video.Video'
        #django_get_or_create = ('video_id',)
    title = factory.Sequence(lambda n: 'YouTube Video Title ' + n)


    youku = factory.SubFactory(YoukuFactory)





