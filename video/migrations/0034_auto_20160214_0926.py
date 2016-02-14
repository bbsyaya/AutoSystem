# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0033_auto_20160209_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='allow_upload_youku',
            field=models.BooleanField(default='True', help_text='\u662f\u5426\u53ef\u4ee5\u4e0a\u4f20\u5230\u4f18\u9177\uff0c\u9ed8\u8ba4\u4e3aTrue'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youku',
            name='description',
            field=models.TextField(default='', help_text='\u89c6\u9891\u63cf\u8ff0\uff0c\u6700\u591a\u80fd\u51992000\u4e2a\u5b57', max_length=300, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youku',
            name='tags',
            field=models.CharField(help_text='\u81ea\u5b9a\u4e49\u6807\u7b7e\u4e0d\u8d85\u8fc710\u4e2a\uff0c\u5355\u4e2a\u6807\u7b7e\u6700\u5c112\u4e2a\u5b57\u7b26\uff0c\u6700\u591a12\u4e2a\u5b57\u7b26\uff086\u4e2a\u6c49\u5b57\uff09\uff0c\u591a\u4e2a\u6807\u7b7e\u4e4b\u95f4\u7528\u9017\u53f7(,)\u9694\u5f00\uff0c\u4e0a\u4f20\u65f6\u5fc5\u9009', max_length=50, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youku',
            name='title',
            field=models.CharField(help_text='\u89c6\u9891\u6807\u9898\uff0c\u80fd\u586b\u51992-50\u4e2a\u5b57\u7b26,\u4e0a\u4f20\u65f6\u5fc5\u9009', max_length=100, blank=True),
            preserve_default=True,
        ),

    ]
