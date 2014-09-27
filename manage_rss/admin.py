# coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin
from .models import Article, Rss, Group, Site, PubInfo
# Register your models here.

class RssInline(admin.TabularInline):
    model = Rss


class ArticleInline(admin.TabularInline):
    model = Article


class PubInfoInline(admin.TabularInline):
    model = PubInfo


class ArticleAdmin(admin.ModelAdmin):
    list_display = (
    'title', 'url', 'grab_date', 'read_status', 'publishable_status', 'group', 'rss', 'pub_info', 'pub_article')

    actions = ['make_publishable']
    #在change list页面选择多项后的，批量操作
    def make_publishable(self, request, queryset):
        queryset.update(review_status=True)
    make_publishable.short_description = "Mark selected articles as publishable"

class RssAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'group', 'url', 'remark', 'article_num')
    inlines = [ArticleInline, ]


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'remark', 'grab_article', 'article_num')
    # 在group的修改页面显示它的rss模块
    inlines = [RssInline, ]


class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'username')


class PubInfoAdmin(admin.ModelAdmin):
    list_display = ('site', 'post_id')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Rss, RssAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Site, SiteAdmin)
admin.site.register(PubInfo, PubInfoAdmin)

