# coding=utf-8
from wordpress_xmlrpc.methods import taxonomies
from manage_rss.models import Article, Site

__author__ = 'GoTop'
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost
from wordpress_xmlrpc.methods.users import GetUserInfo


def new_post(site_id, article_id, category=None, post_tag=None):
    site = Site.objects.get(pk=site_id)
    client = Client(site.url + '/xmlrpc.php', site.username, site.password)

    article = Article.objects.get(pk=article_id)

    post = WordPressPost()
    post.title = article.title
    post.content = article.context
    # ## post.post_status='publish'
    # ## 文章默认发布为草稿
    post.post_status = 'publish'

    if category:
        post.terms_names = {'category': category}
    if post_tag:
        post.terms_names = {'post_tag': post_tag}

    post_id = client.call(NewPost(post))
    return post_id


def get_categories(site_id):
    '''
    获取site_id的所有category
    :param site_id:
    :return:
    '''
    site = Site.objects.get(pk=site_id)
    client = Client(site.url + '/xmlrpc.php', site.username, site.password)
    categories = client.call(taxonomies.GetTerms('category'))
    return categories