# coding=utf-8
from __future__ import unicode_literals, absolute_import

import pyexcel as pe

from AutoSystem.settings import TAOBAOKE_EXCEL_FILE
from ad.models import TaoBao

__author__ = 'GoTop'


def import_taobaoke_excel():
    records = pe.iget_records(file_name=TAOBAOKE_EXCEL_FILE)

    for record in records:
        taobao, created = TaoBao.objects.update_or_create(
            item_id=record['商品id'],
            defaults={'shop_name': record['店铺名称'],
                      'seller_id': record['商品id'],
                      'title': record['商品名称'],
                      'pic_url': record['商品主图'],
                      'item_url': record['商品详情页链接地址'],
                      'price': record['商品价格(单位：元)'],
                      'volume': record['商品月销量'],
                      #'commission_num': record['商品id'],
                      'commission': record['佣金'],
                      'commission_rate': record['收入比率(%)'],
                      'item_click_short_url': record['淘宝客短链接(300天内有效)'],
                      'item_click_long_url': record['淘宝客链接'],

                      }
        )
        TaoBao.objects.get_or_create(item_id=record['商品id'])
        print("%s is aged at %s" % (record['商品id'], record['商品名称']))
    return records
