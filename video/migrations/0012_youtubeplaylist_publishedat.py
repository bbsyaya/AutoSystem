# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0011_auto_20160525_0051'),
    ]

    operations = [
        migrations.AddField(
            model_name='youtubeplaylist',
            name='publishedAt',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
