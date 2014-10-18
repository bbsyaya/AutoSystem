# coding=utf-8
# encoding = utf-8
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.db import models
from tinymce.models import HTMLField
from autoslug import AutoSlugField

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=100)
    remark = models.CharField(max_length=300, null=True, blank=True)
    slug = AutoSlugField(populate_from='name', always_update=True)
    site = models.ForeignKey('Site')

    def __str__(self):
        return self.name

    def article_num(self):
        rss_set = Rss.objects.filter(group = self)
        article_num = 0
        for rss in rss_set:
            article_num = article_num +Article.objects.filter(rss=rss).count()
        return article_num
    article_num.short_description = 'Article Num'

    def grab_article(self):
        html = "<a href='%s' target='_blank'>Grab</a>" % reverse("grab_article_of_group", args=[self.pk])
        return html

    # If you'd rather not escape the output of the method, give the method an allow_tags attribute whose value is True
    grab_article.allow_tags = True
    grab_article.short_description = 'Grab Article'

    def rss_url(self):
        html = "<a href='%s' target='_blank'>Rss Url</a>" % reverse("group_rss_url", args=[self.slug])
        return html

    # If you'd rather not escape the output of the method, give the method an allow_tags attribute whose value is True
    rss_url.allow_tags = True
    rss_url.short_description = 'Rss Url'


class Rss(models.Model):
    TYPE_CHOICE = (
        ('google_alert', 'Google Alert'),
        ('normal_rss', 'Normal Rss'),
    )

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TYPE_CHOICE, default='normal_rss')
    url = models.URLField(max_length=300)
    remark = models.CharField(max_length=300, null=True, blank=True)
    group = models.ForeignKey('Group', null=True, blank=True, related_name='related_rss')


    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "rss"

    def article_num(self):
        return Article.objects.filter(rss=self.id).count()
    article_num.short_description = 'Article Num'


class Article(models.Model):
    READ_STATUS_CHOICE = (
        ('u', 'unRead'),
        ('r', 'Read'),
    )

    REVIEW_CHOICE = (
        ('p', 'Publishable'),
        ('d', 'Decline'),
    )

    url = models.URLField(max_length=300)
    title = models.CharField(max_length=300)
    context = HTMLField()
    published = models.DateTimeField(null=True, blank=True)
    read_status = models.BooleanField(default=False)#TRUE表明已经生成RSS，FALSE表明未生成RSS
    editable_status = models.BooleanField(default=False)#TRUE表明需要修改，FALSE表明不需要
    publishable_status = models.BooleanField(default=False)#TRUE表明可以发布，FALSE表明不能发布
    grab_date = models.DateTimeField(auto_now_add=True)
    rss = models.ForeignKey('Rss', related_name='articles')
    pub_info = models.ForeignKey('PubInfo', null=True, blank=True)


    def group(self):
        return self.rss.group

    group.short_description = 'Group'




    def pub_article(self):
        if self.pub_info:
            post_link = self.pub_info.site.url + '?p=' + self.pub_info.post_id
            html = "<a href='%s' target='_blank'>Link</a>" % post_link
        else:
            html = "<a href='%s' target='_blank'>Pub</a>" % reverse("pub_article_url",
                                                                    args=[self.rss.group.site.pk, self.pk])
        return html

    # If you'd rather not escape the output of the method, give the method an allow_tags attribute whose value is True
    pub_article.allow_tags = True
    pub_article.short_description = 'Pub Article'

    # https://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse
    def get_absolute_url(self):
        return reverse('article_url', kwargs={'article_id': str(self.id)})

    #https://docs.djangoproject.com/en/dev/ref/unicode/#choosing-between-str-and-unicode
    #如果用__str__,当title里有非utf8字符时，admin界面的删除会出错
    def __unicode__(self):
        return self.title


class Site(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=300)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class PubInfo(models.Model):
    site = models.ForeignKey('Site')
    post_id = models.CharField(max_length=6)
    pub_date = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        str = self.site.name + ' ' + self.post_id
        return str
