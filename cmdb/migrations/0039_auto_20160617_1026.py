# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0038_auto_20160617_1015'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='email_password',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='media',
            name='email_user',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
    ]
