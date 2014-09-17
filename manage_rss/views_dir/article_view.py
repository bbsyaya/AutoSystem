# coding=utf-8
from __future__ import unicode_literals
from django.shortcuts import render_to_response, get_object_or_404
from manage_rss.function.wordpress import new_post
from manage_rss.models import Rss, Article, Group
from urllib import unquote

__author__ = 'GoTop'
import feedparser


def get_rss_article_view(request, group_name):
    """
    获取google alert的rss链接的文章并保存
    :param request:
    :return:
    """
    group = Group.objects.get(name__exact=group_name)
    rss_queryset = Rss.objects.filter(group=group)

    articles = []
    for rss in rss_queryset:
        feed = feedparser.parse(rss.url)

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


def set_publish_status_view(request, article_id, publish_status):
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

    if publish_status in REVIEW_CHOICE:
        article.pub_status = publish_status
        article.save()
        result = article.title + '已设置为' + publish_status
    else:
        result = publish_status + '不在指定的队列里'

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
    article.pub_status = 'published'
    article.save()
    return render_to_response('result.html', {'text': article.title + '已发布id为article_id的文章，post id为 post_id'})