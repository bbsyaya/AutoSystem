# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0005_auto_20140831_2128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rss',
            options={'verbose_name_plural': 'rss'},
        ),
        migrations.AlterField(
            model_name='group',
            name='remark',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
