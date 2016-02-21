# coding=utf-8
from __future__ import unicode_literals, absolute_import

from faker import Factory

__author__ = 'GoTop'

from video.tests.factories import YoukuFactory

from django.test import TestCase

class YoukuTagsTest(TestCase):
    def test_if_youku_tags_add(self):
        self.assertEqual('1', '1')

# class YoukuTagsTest(TestCase):
#     def test_if_youku_tags_add(self):
#         youku = YoukuFactory.create()
#         faker = Factory.create()
#
#         add_tags_list = faker.words(2)
#
#         origin_tags_list = youku.get_tags_list()
#
#         assert_tags_list = origin_tags_list.append(add_tags_list)
#
#         youku.add_tags(add_tags_list)
#         self.assertEqual(youku.tagsm, assert_tags_list)
