# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0015_group_site'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='review_status',
        ),
        migrations.AddField(
            model_name='article',
            name='publishable_status',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='read_status',
            field=models.BooleanField(default=False),
        ),
    ]
