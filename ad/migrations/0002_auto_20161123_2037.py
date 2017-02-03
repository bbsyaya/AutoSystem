# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('ad', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taobao',
            name='num_iid',
        ),
        migrations.AddField(
            model_name='taobao',
            name='item_id',
            field=models.CharField(default='', help_text=b'\xe6\xb7\x98\xe5\xae\x9d\xe5\xae\xa2\xe5\x95\x86\xe5\x93\x81\xe6\x95\xb0\xe5\xad\x97id', max_length=50, primary_key=True),
            preserve_default=False,
        ),
    ]
