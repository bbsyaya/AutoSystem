# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0003_auto_20161123_2038'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taobao',
            name='commission_num',
        ),
    ]
