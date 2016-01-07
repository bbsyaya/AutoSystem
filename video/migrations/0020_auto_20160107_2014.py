# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('video', '0019_auto_20160107_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='description',
            field=models.TextField(max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='youku',
            name='category',
            field=models.CharField(default='Others', max_length=50, null=True, blank=True, choices=[('Games', '\u6e38\u620f'), ('Tech', '\u79d1\u6280'), ('News', '\u8d44\u8baf'), ('LifeStyle', '\u751f\u6d3b'), ('Original', '\u539f\u521b'), ('TV', '\u7535\u89c6\u5267'), ('Entertainment', '\u5a31\u4e50'), ('Movies', '\u7535\u5f71'), ('Sports', '\u4f53\u80b2'), ('Music', '\u97f3\u4e50'), ('Anime', '\u52a8\u6f2b'), ('Fashion', '\u65f6\u5c1a'), ('Parenting', '\u4eb2\u5b50'), ('Autos', '\u6c7d\u8f66'), ('Travel', '\u65c5\u6e38'), ('Education', '\u6559\u80b2'), ('Humor', '\u641e\u7b11'), ('Ads', '\u5e7f\u544a'), ('Others', '\u5176\u4ed6')]),
        ),
        migrations.AlterField(
            model_name='youku',
            name='tags',
            field=models.CharField(help_text='\u81ea\u5b9a\u4e49\u6807\u7b7e\u4e0d\u8d85\u8fc710\u4e2a\uff0c\u5355\u4e2a\u6807\u7b7e\u6700\u5c112\u4e2a\u5b57\u7b26\uff0c\u6700\u591a12\u4e2a\u5b57\u7b26\uff086\u4e2a\u6c49\u5b57\uff09\uff0c\u591a\u4e2a\u6807\u7b7e\u4e4b\u95f4\u7528\u9017\u53f7(,)\u9694\u5f00', max_length=50, null=True, blank=True),
        ),

    ]
