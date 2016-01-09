# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0020_auto_20160107_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='youku_playlist_category',
            field=models.CharField(default='Others', max_length=50, null=True, blank=True, choices=[('Games', '\u6e38\u620f'), ('Tech', '\u79d1\u6280'), ('News', '\u8d44\u8baf'), ('LifeStyle', '\u751f\u6d3b'), ('Original', '\u539f\u521b'), ('TV', '\u7535\u89c6\u5267'), ('Entertainment', '\u5a31\u4e50'), ('Movies', '\u7535\u5f71'), ('Sports', '\u4f53\u80b2'), ('Music', '\u97f3\u4e50'), ('Anime', '\u52a8\u6f2b'), ('Fashion', '\u65f6\u5c1a'), ('Parenting', '\u4eb2\u5b50'), ('Autos', '\u6c7d\u8f66'), ('Travel', '\u65c5\u6e38'), ('Education', '\u6559\u80b2'), ('Humor', '\u641e\u7b11'), ('Ads', '\u5e7f\u544a'), ('Others', '\u5176\u4ed6')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='youku',
            name='description',
            field=models.TextField(max_length=300, null=True, blank=True),
        ),

    ]
