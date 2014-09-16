from django.contrib import admin
from manage_rss.models import Article, Rss, Group, Site
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'grab_date','read_status','pub_status', 'publish_date', 'rss')


class RssAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'group', 'url', 'remark')


class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'keywords', 'remark')

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'username')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Rss, RssAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Site, SiteAdmin)

