# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0018_auto_20160107_1143'),
    ]

    operations = [
        migrations.RenameField(
            model_name='youku',
            old_name='youku',
            new_name='video',
        ),
    ]
