# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0004_userprofile_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='position',
            field=models.SmallIntegerField(blank=True, null=True, choices=[(0, b'\xe4\xba\xa7\xe5\x93\x81\xe7\xbb\x8f\xe7\x90\x86'), (1, b'\xe6\xb5\x8b\xe8\xaf\x95\xe7\xbb\x8f\xe7\x90\x86'), (2, b'\xe5\xbc\x80\xe5\x8f\x91\xe7\xbb\x8f\xe7\x90\x86'), (3, b'\xe8\xbf\x90\xe7\xbb\xb4\xe4\xba\xba\xe5\x91\x98'), (4, b'\xe8\xbf\x90\xe7\xbb\xb4\xe7\xbb\x8f\xe7\x90\x86'), (5, b'\xe6\x8a\x80\xe6\x9c\xaf\xe7\xbb\x8f\xe7\x90\x86')]),
        ),
    ]
