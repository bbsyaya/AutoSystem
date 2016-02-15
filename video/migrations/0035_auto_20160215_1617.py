# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0034_auto_20160214_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='duration',
            field=models.IntegerField(help_text='\u89c6\u9891\u65f6\u957f\uff0c\u5355\u4f4d\u662fs', max_length=10, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='like_count',
            field=models.CharField(max_length=10, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='tags',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='view_count',
            field=models.CharField(max_length=10, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youku',
            name='tags',
            field=models.CharField(help_text='\u81ea\u5b9a\u4e49\u6807\u7b7e\u4e0d\u8d85\u8fc710\u4e2a\uff0c\u5355\u4e2a\u6807\u7b7e\u6700\u5c112\u4e2a\u5b57\u7b26\uff0c\u6700\u591a 12 \u4e2a\u5b57\u7b26\uff086\u4e2a\u6c49\u5b57\uff09\uff0c\u591a\u4e2a\u6807\u7b7e\u4e4b\u95f4\u7528\u9017\u53f7(,)\u9694\u5f00\uff0c\u4e0a\u4f20\u65f6\u5fc5\u9009', max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
