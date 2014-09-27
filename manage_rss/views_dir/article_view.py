# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render_to_response, get_object_or_404
from manage_rss.function.rss import gen_fivefilters_rss
from manage_rss.function.wordpress import new_post, get_categories
from manage_rss.models import Rss, Article, Group, PubInfo, Site
from urllib import unquote

__author__ = 'GoTop'
import feedparser


def get_rss_article_view(request, group_id):
    """
    获取rss链接的文章并保存
    :param request:
    :return:
    """
    group = Group.objects.get(pk__exact=group_id)
    rss_queryset = Rss.objects.filter(group=group)

    articles = []
    for rss in rss_queryset:
        fivefilters_full_article_rss = gen_fivefilters_rss(rss.url)
        feed = feedparser.parse(fivefilters_full_article_rss)

        for i in range(0, len(feed['entries'])):
            title = feed['entries'][i].title
            description = feed['entries'][i].summary

            # 如果使用fivefilters.org来获取rss的全文链接，需要在获取的文章后去除一段说明
            description = description.replace(
                "This entry passed through the Full-Text RSS service - if this is your content and you're reading it on someone else's site, please read the FAQ at fivefilters.org/content-only/faq.php#publishers.",
                '')

            url = feed['entries'][i].link
            url = unquote(url)
            # 将google alert的rss中的链接去掉google网站的前缀和后缀
            url = url.split('&ct')
            url = url[0].replace("https://www.google.com/url?rct=j&sa=t&url=", '')

            (article, created) = Article.objects.get_or_create(url__exact=url,
                                                               defaults={'title': title, 'context': description,
                                                                         'url': url,
                                                                         'rss': rss})

            articles.append(article)

    return render_to_response('result.html', {'list': articles})


def set_publishable_status_view(request, article_id, publishable_status):
    """
    设置文章的publish_status
    :param request:
    :param article_id:
    :return:
    """
    article = get_object_or_404(Article, pk=article_id)

    REVIEW_CHOICE = (
        ('publishable', 'Publishable'),
        ('decline', 'Decline'),
    )

    if publishable_status == 1:
        publishable_status = True
    elif publishable_status == 0:
        publishable_status = False

    article.publishable_status = publishable_status
    article.save()
    result = article.title + '已设置为' + str(publishable_status)

    return render_to_response('result.html', {'text': result})


def pub_article_view(request, site_id, article_id):
    """
    发布文章
    :param request:
    :param article_id:
    :return:
    """
    article = get_object_or_404(Article, pk=article_id)
    post_id = new_post(site_id, article_id)
    site = Site.objects.get(pk=site_id)
    pub_info = PubInfo.objects.create(site=site, post_id=post_id)
    article.pub_status = 'published'
    article.pub_info = pub_info
    article.save()
    return render_to_response('result.html', {'text': article.title + '已发布id为article_id的文章，post id为 post_id'})


def get_categories_view(request, site_id):
    categories = get_categories(site_id)
    return render_to_response('result.html', {'list': categories})