# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0015_auto_20160106_2238'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='baiduy_yun',
            new_name='baidu_yun',
        ),
    ]
