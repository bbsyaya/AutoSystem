# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0017_auto_20141003_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='published',
            field=models.DateTimeField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='rss',
            field=models.ForeignKey(related_name='articles', to='manage_rss.Rss'),
        ),
    ]
