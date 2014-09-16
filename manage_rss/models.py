from django.db import models
from tinymce.models import HTMLField

# Create your models here.

class Group(models.Model):
    name = models.CharField(max_length=100)
    keywords = models.CharField(max_length=100)
    remark = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.name


class Rss(models.Model):
    TYPE_CHOICE = (
        ('google_alert', 'Google Alert'),
        ('normal_rss', 'Normal Rss'),
    )

    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=TYPE_CHOICE, default='normal_rss')
    url = models.CharField(max_length=300)
    remark = models.CharField(max_length=300)
    group = models.ForeignKey('Group')


    def __str__(self):
        return self.name


    class Meta:
        verbose_name_plural = "rss"


class Article(models.Model):
    READ_STATUS_CHOICE = (
        ('u', 'unRead'),
        ('r', 'Read'),
    )

    PUB_STATUS_CHOICE = (
        ('unpublish', 'unPublish'),
        ('published', 'Published'),
        ('publishable', 'Publishable'),
        ('decline', 'Decline'),
    )

    url = models.URLField(max_length=300)
    title = models.CharField(max_length=300)
    context = HTMLField()
    read_status = models.CharField(max_length=1, choices=READ_STATUS_CHOICE, default='u')
    pub_status = models.CharField(max_length=1, choices=PUB_STATUS_CHOICE, default='unpublish')
    grab_date = models.DateTimeField(auto_now_add=True)
    publish_date = models.DateTimeField(null=True, blank=True)
    rss = models.ForeignKey('Rss')


    # https://docs.djangoproject.com/en/dev/ref/urlresolvers/#django.core.urlresolvers.reverse
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('article_url', kwargs={'article_id': str(self.id)})


class Site(models.Model):
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=300)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
