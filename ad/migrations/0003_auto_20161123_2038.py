# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0002_auto_20161123_2037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taobao',
            name='item_id',
            field=models.CharField(help_text=b'\xe6\xb7\x98\xe5\xae\x9d\xe5\xae\xa2\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe5\xad\x97id', max_length=50, serialize=False, primary_key=True),
        ),
        migrations.AlterField(
            model_name='taobao',
            name='seller_id',
            field=models.CharField(help_text=b'\xe5\x8d\x96\xe5\xae\xb6id', max_length=50),
        ),
    ]
