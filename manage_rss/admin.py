# coding=utf-8
from __future__ import unicode_literals

from django.contrib import admin
from manage_rss.models import Article, Rss, Group, Site, PubInfo
# Register your models here.

class RssInline(admin.TabularInline):
    model = Rss

class PubInfoInline(admin.TabularInline):
    model = PubInfo


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'grab_date', 'read_status', 'review_status', 'rss', 'pub_info', 'pub_article')

    actions = ['make_publishable']


    def make_publishable(self, request, queryset):
        queryset.update(review_status='p')

    make_publishable.short_description = "Mark selected articles as publishable"


class RssAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'group', 'url', 'remark')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'remark')
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

