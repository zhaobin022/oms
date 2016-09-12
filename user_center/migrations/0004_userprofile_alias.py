# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0003_auto_20160523_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='alias',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
