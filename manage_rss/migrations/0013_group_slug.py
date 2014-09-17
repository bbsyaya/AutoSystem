# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('manage_rss', '0012_auto_20140917_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=1, editable=False),
            preserve_default=False,
        ),
    ]
