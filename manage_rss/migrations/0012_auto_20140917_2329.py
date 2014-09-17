# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0011_auto_20140917_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='keywords',
        ),
        migrations.AlterField(
            model_name='rss',
            name='group',
            field=models.ForeignKey(blank=True, to='manage_rss.Group', null=True),
        ),
        migrations.AlterField(
            model_name='rss',
            name='remark',
            field=models.CharField(max_length=300, null=True, blank=True),
        ),
    ]
