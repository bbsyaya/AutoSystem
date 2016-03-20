# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0002_auto_20160222_2359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youku',
            name='tags',
            field=models.CharField(help_text='\u81ea\u5b9a\u4e49\u6807\u7b7e\u4e0d\u8d85\u8fc710\u4e2a\uff0c\u5355\u4e2a\u6807\u7b7e\u6700\u5c112\u4e2a\u5b57\u7b26\uff0c\u6700\u591a 12 \u4e2a\u5b57\u7b26\uff086\u4e2a\u6c49\u5b57\uff09\uff0c\u591a\u4e2a\u6807\u7b7e\u4e4b\u95f4\u7528\u4e2d\u6587\u7684\u9017\u53f7(,)\u9694\u5f00\uff0c\u4e0a\u4f20\u65f6\u5fc5\u9009', max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='yt_channel',
            name='description',
            field=models.TextField(max_length=500, blank=True),
        ),
    ]
