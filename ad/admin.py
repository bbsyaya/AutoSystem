# coding=utf-8
from __future__ import unicode_literals

__author__ = 'GoTop'
from django.utils.html import format_html
from django.contrib import admin
from ad.models import TaoBao


class TaoTaoAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'shop_name', 'show_item_pic', 'show_item_url',
        'price', 'volume',
        'commission', 'commission_rate',
        'show_item_click_short_url'
    )

    def show_item_pic(self, obj):
        return format_html("<img src={url} height='42' width='42' />", url=obj.pic_url)
    show_item_pic.short_description = "图片"

    def show_item_url(self, obj):
        return format_html("<a href='{url}'>淘宝链接</a>", url=obj.item_url)
    show_item_url.short_description = "淘宝链接"

    def show_item_click_short_url(self, obj):
        return format_html("<a href='{url}'>淘客短链接</a>", url=obj.item_click_short_url)

    show_item_click_short_url.short_description = "淘客短链接"


admin.site.register(TaoBao, TaoTaoAdmin)
