# coding=utf-8
from __future__ import unicode_literals, absolute_import

from faker import Factory

from video.function.youku import set_youku_category_local
from video.models import Youku

__author__ = 'GoTop'

from video.tests.factories import YoukuFactory
from faker import Factory
from model_mommy import mommy
from django.test import TestCase


# class YoukuTagsTest(TestCase):
#     def test_if_youku_tags_add(self):
#         self.assertEqual('1', '1')

class YoukuTagsTest(TestCase):
    def test_if_youku_tags_add(self):
        """
        测试是否能添加list形式的tags到youku model中
        :return:
        """

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

    def test_set_youku_category(self):
        """
        测试set_youku_category()是否正常
        :return:
        """
        youku = YoukuFactory.create()

        youku_new = set_youku_category_local(youku.id)
        self.assertEqual(youku_new.category,
                         youku.video.channel.category.get_youku_playlist_category_display())

        # def test_set_youku_category_2(self):
        #     youku = mommy.make(Youku,
        #
        # Youku__Video__Channel__category__youku_playlist_category='游戏')
        #     set_youku_category(youku.id)
        #     self.assertEqual(youku.category,
        #                      youku.video.channel.category.get_youku_playlist_category_display())
