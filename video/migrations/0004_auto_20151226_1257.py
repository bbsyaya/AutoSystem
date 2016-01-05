# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0003_auto_20151225_2258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='url',
        ),
        migrations.AlterField(
            model_name='video',
            name='publishedAt',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
