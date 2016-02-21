# coding=utf-8
from __future__ import unicode_literals, absolute_import

from faker import Factory

__author__ = 'GoTop'

from video.tests.factories import YoukuFactory
from faker import Factory
from django.test import TestCase


# class YoukuTagsTest(TestCase):
#     def test_if_youku_tags_add(self):
#         self.assertEqual('1', '1')

class YoukuTagsTest(TestCase):
    def test_if_youku_tags_add(self):
        # With Django versions 1.8.0 to 1.8.3, it was no longer possible to
        # call .build() on a factory if this factory used a SubFactory
        # pointing to another model: Django refused to set a ForeignKey to an
        #  unsaved Model instance.
        youku = YoukuFactory.create()
        faker = Factory.create()

        add_tags_list = faker.words(2)

        origin_tags_list = youku.get_tags_list()

        assert_tags_list = origin_tags_list + add_tags_list

        youku.add_tags(add_tags_list)
        self.assertEqual(youku.get_tags_list(), assert_tags_list)
