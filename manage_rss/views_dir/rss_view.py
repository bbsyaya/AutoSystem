# coding=utf-8
from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from manage_rss.models import Rss, Article, Site

__author__ = 'GoTop'


class unpub_article_feed(Feed):
    """
    从Article数据表中获取没有未发布的文章，生成rss
    """

    def get_object(self, request, keywords):
        return get_object_or_404(Rss, remark__exact=keywords)


    def title(self, obj):
        # 参数obj为get_object(self, request, keywords)的返回值
        return "Articles for keywords \"%s\" " % obj.remark


    def link(self, obj):
        return obj.url


    def description(self, obj):
        return "Articles for keywords \"%s\" " % obj.remark


    def items(self, obj):
        return Article.objects.filter(pub_status__exact='u').order_by('-publish_date')[:10]

    def item_title(self, item):
        # 参数item为方法items()返回的单个对象
        return item.title


    def item_description(self, item):
        from django.core.urlresolvers import reverse

        site_id = 1
        site = Site.objects.get(pk=site_id)
        set_article_status_url = site.url + reverse('set_article_status_url', kwargs={'article_id': int(item.id),
                                                                                      'publish_status': 'publishable'})

        article_url = site.url + reverse('article_url', kwargs={'article_id': int(item.id)})
        context = item.context + u"<p><a href=' %s '>set_article_status</a>  <p><a href=' %s '>article_url</a>" % (
        set_article_status_url, article_url)
        return context


def item_link(self, item):
    return item.url