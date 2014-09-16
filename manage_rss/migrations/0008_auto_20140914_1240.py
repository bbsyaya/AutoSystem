# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0007_auto_20140901_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='pub_status',
            field=models.CharField(default=b'unpublish', max_length=1, choices=[(b'unpublish', b'unPublish'), (b'published', b'Published'), (b'publishable', b'Publishable'), (b'decline', b'Decline')]),
        ),
    ]
