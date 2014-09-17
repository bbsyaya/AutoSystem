# coding=utf-8
from django.conf.urls import url
from manage_rss import views

from manage_rss.views_dir.article_view import get_rss_article_view, pub_article_view, \
    set_publish_status_view
from manage_rss.views_dir.rss_view import unpub_article_feed

urlpatterns = [
    # 获取google alert的rss链接的文章并保存
    # 例如 http://127.0.0.1:8000/manage_rss/get_rss_article
    url(r'^get_rss_article$', get_rss_article_view),

    #使用下载到本地Article数据表中的文章生成RSS
    #例如 http://127.0.0.1:8000/manage_rss/acmilan/rss/
    url(r'^(?P<keywords>[-\w]+)/rss/$', unpub_article_feed()),

    #查看保存到本地的单篇文章(未完成)
    #例如 http://127.0.0.1:8000/manage_rss/article/5/
    url(r'^article/(?P<article_id>\d+)/$', views.article_view, name='article_url'),

    #设置文章的publish_status
    #例如 http://127.0.0.1:8000/manage_rss/set_publish_status/5/decline/
    url(r'^set_publish_status/(?P<article_id>\d+)/(?P<publish_status>\w+)/$', set_publish_status_view,
        name='set_article_status_url'),

    #发布文章
    #例如 http://127.0.0.1:8000/manage_rss/pub_article/1/5/
    url(r'^pub_article/(?P<site_id>\d+)/(?P<article_id>\d+)/$', pub_article_view),
]