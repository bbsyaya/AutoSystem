# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='taobao',
            fields=[
                ('num_iid', models.CharField(help_text=b'\xe6\xb7\x98\xe5\xae\x9d\xe5\xae\xa2\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe5\xad\x97id', max_length=50, null=True, blank=True)),
                ('shop_name', models.CharField(help_text=b'\xe5\xba\x97\xe9\x93\xba\xe5\x90\x8d\xe7\xa7\xb0', max_length=200)),
                ('seller_id', models.CharField(help_text=b'\xe5\x8d\x96\xe5\xae\xb6id', max_length=50, serialize=False, primary_key=True)),
                ('title', models.CharField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe5\x90\x8d\xe7\xa7\xb0', max_length=200)),
                ('pic_url', models.URLField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe4\xb8\xbb\xe5\x9b\xbe', max_length=300, blank=True)),
                ('item_url', models.URLField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe8\xaf\xa6\xe6\x83\x85\xe9\xa1\xb5\xe9\x93\xbe\xe6\x8e\xa5\xe5\x9c\xb0\xe5\x9d\x80', max_length=300, blank=True)),
                ('price', models.DecimalField(help_text=b'\xe5\x95\x86\xe5\x93\x81\xe4\xbb\xb7\xe6\xa0\xbc(\xe5\x8d\x95\xe4\xbd\x8d\xef\xbc\x9a\xe5\x85\x83)', max_digits=8, decimal_places=2)),
                ('volume', models.PositiveIntegerField(help_text=b'30\xe5\xa4\xa9\xe5\x86\x85\xe4\xba\xa4\xe6\x98\x93\xe9\x87\x8f')),
                ('commission_num', models.PositiveIntegerField(help_text=b'\xe7\xb4\xaf\xe8\xae\xa1\xe6\x88\x90\xe4\xba\xa4\xe9\x87\x8f.\xe6\xb3\xa8\xef\xbc\x9a\xe8\xbf\x94\xe5\x9b\x9e\xe7\x9a\x84\xe6\x95\xb0\xe6\x8d\xae\xe6\x98\xaf30\xe5\xa4\xa9\xe5\x86\x85\xe7\xb4\xaf\xe8\xae\xa1\xe6\x8e\xa8\xe5\xb9\xbf\xe9\x87\x8f')),
                ('commission', models.DecimalField(help_text=b'\xe4\xbd\xa3\xe9\x87\x91', max_digits=8, decimal_places=2)),
                ('commission_rate', models.DecimalField(help_text=b'\xe6\x94\xb6\xe5\x85\xa5\xe6\xaf\x94\xe4\xbe\x8b', max_digits=3, decimal_places=2)),
                ('item_click_short_url', models.URLField(help_text=b'\xe6\xb7\x98\xe5\xae\x9d\xe5\xae\xa2\xe7\x9f\xad\xe9\x93\xbe\xe6\x8e\xa5(300\xe5\xa4\xa9\xe5\x86\x85\xe6\x9c\x89\xe6\x95\x88)', max_length=300, blank=True)),
                ('item_click_long_url', models.URLField(help_text=b'\xe6\xb7\x98\xe5\xae\x9d\xe5\xae\xa2\xe9\x93\xbe\xe6\x8e\xa5', max_length=300, blank=True)),
            ],
        ),
    ]
