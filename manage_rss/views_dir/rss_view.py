# coding=utf-8
from __future__ import unicode_literals
from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from manage_rss.models import Rss, Article, Site, Group
from django.contrib.sites.models import Site

__author__ = 'GoTop'


class unpub_article_feed(Feed):
    """
    从Article数据表中获取没有未发布的文章，生成rss
    """

    def get_object(self, request, group_slug):
        return get_object_or_404(Group, slug__exact=group_slug)

    def title(self, obj):
        # 参数obj为get_object(self, request, keywords)的返回值
        return "Articles for keywords \"%s\" " % obj.name


    def link(self, obj):
        # https://docs.djangoproject.com/en/dev/ref/contrib/admin/#admin-reverse-urls
        from django.core import urlresolvers

        group_change_url = urlresolvers.reverse('admin:manage_rss_group_change', args=(obj.id,))
        return group_change_url


    def description(self, obj):
        return "Articles for Group \"%s\" " % obj.name


    def items(self, obj):
        # https://docs.djangoproject.com/en/dev/topics/db/queries/#backwards-related-objects
        rss_set = obj.related_rss.all()
        all_article_set = []
        for rss in rss_set:
            #在使用SQLite的时候，因为其没有boolean型，所以django model中的boolean型在SQLite中保存数字1,0
            #所以在使用SQLite时，设置publishable_status__exact=0
            #在使用其他数据库时，设置publishable_status__exact=False
            article_set = Article.objects.filter(rss__exact=rss).filter(read_status__exact=True).order_by(
                '-grab_date')[:10]

            Article.objects.filter(pk__in=article_set).update(read_status=True)
            all_article_set = all_article_set + list(article_set)

        #用 article_set.update(read_status=True) 会提示Cannot update a query once a slice has been taken
        #因为对queryset进行了slice之后无法再用update。参考 http://stackoverflow.com/a/4286037/1314124
        #以下方法来自 http://stackoverflow.com/a/4286144/1314124

        return all_article_set

    def item_title(self, item):
        # 参数item为方法items()返回的单个对象
        return item.title


    def item_description(self, item):
        from django.core.urlresolvers import reverse

        # https://docs.djangoproject.com/en/dev/ref/contrib/sites/#getting-the-current-domain-for-full-urls
        #使用django自带的Site模块获取网站的网址
        set_publishable_status_url = Site.objects.get_current().domain + reverse('set_publishable_status_url',
                                                                                 kwargs={'article_id': int(item.id),
                                                                                         'publishable_status': '1'})

        set_editable_status_url = Site.objects.get_current().domain + reverse('set_editable_status_url',
                                                                                 kwargs={'article_id': int(item.id),
                                                                                         'editable_status': '1'})

        article_url = Site.objects.get_current().domain + reverse('article_url', kwargs={'article_id': int(item.id)})

        #在正文的后面加入可以发布文章的链接
        context = item.context + "<p><a href=' %s '>set_publishable_status</a>  <p><a href=' %s '>set_editable_status</a> " \
                                 "<p><a href=' %s '>article_url</a>" % (
            set_publishable_status_url, set_editable_status_url, article_url)
        return context

    def item_pubdate(self, item):
        return item.published

    def item_link(self, item):
        return item.url

