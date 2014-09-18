# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0013_group_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_info',
            field=models.ForeignKey(blank=True, to='manage_rss.PubInfo', null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='review_status',
            field=models.CharField(default=b'd', max_length=1, choices=[(b'p', b'Publishable'), (b'd', b'Decline')]),
        ),
    ]
