# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0007_auto_20160405_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='youku',
            name='tags',
            field=models.TextField(help_text='\u4e0d\u8d85\u8fc710\u4e2a;\u5355\u4e2a\u6807\u7b7e\u6700\u5c112\u4e2a\u3001\u6700\u591a12\u4e2a\u5b57\u7b26;\u6807\u7b7e\u95f4\u7528\u82f1\u6587\u7684\u9017\u53f7(,)\u548c\u7a7a\u683c\u9694\u5f00\uff0c\u5355\u4e2atag\u4e2d\uff0c\u4e0d\u5141\u8bb8\u6709_ - ;\u5fc5\u9009', max_length=200, blank=True),
        ),
    ]
