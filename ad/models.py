# coding=utf-8
from django.db import models

# Create your models here.



class taobao(models.Model):
    """
    http://open.taobao.com/docs/api.htm?spm=a219a.7395905.0.0.oWQqfP&apiId=23803
    """
    num_iid = models.CharField(max_length=50, null=True, blank=True,help_text='淘宝客商品数字id')
    shop_name = models.CharField(max_length=200, help_text='店铺名称')
    seller_id = models.CharField(max_length=50, primary_key=True,help_text='卖家id')

    title = models.CharField(max_length=200,help_text='商品名称' )
    pic_url = models.URLField(max_length=300, blank=True,help_text='商品主图')
    item_url = models.URLField(max_length=300, blank=True, help_text='商品详情页链接地址')

    price = models.DecimalField(max_digits=8, decimal_places=2,help_text='商品价格(单位：元)')
    volume = models.PositiveIntegerField(help_text='30天内交易量')
    commission_num = models.PositiveIntegerField(help_text='累计成交量.注：返回的数据是30天内累计推广量')
    commission = models.DecimalField(max_digits=8, decimal_places=2,help_text='佣金')
    commission_rate = models.DecimalField(max_digits=3, decimal_places=2,help_text='收入比例')

    item_click_short_url = models.URLField(max_length=300, blank=True,help_text='淘宝客短链接(300天内有效)')
    item_click_long_url = models.URLField(max_length=300, blank=True,help_text='淘宝客链接')
