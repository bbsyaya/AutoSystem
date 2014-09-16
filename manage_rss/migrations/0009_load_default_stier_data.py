# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from manage_rss.models import Site


def load_data(apps, schema_editor):
    Site(
        name='autoblog',
        url='http://127.0.0.1:808/autoblog',
        username='admin',
        password='123456'
    ).save()


class Migration(migrations.Migration):
    dependencies = [
        ('manage_rss', '0008_auto_20140914_1240'),
    ]

    operations = [
        migrations.RunPython(load_data)
    ]
