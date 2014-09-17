from django.contrib import admin
from manage_rss.models import Article, Rss, Group, Site
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'grab_date', 'read_status', 'review_status', 'rss')
    actions = ['make_publishable']


    def make_publishable(self, request, queryset):
        queryset.update(review_status='p')

    make_publishable.short_description = "Mark selected articles as publishable"



class RssAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'group', 'url', 'remark')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug','remark')


class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'username')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Rss, RssAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Site, SiteAdmin)

