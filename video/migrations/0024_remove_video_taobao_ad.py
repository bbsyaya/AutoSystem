# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0023_auto_20170203_2147'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='taobao_ad',
        ),
    ]
