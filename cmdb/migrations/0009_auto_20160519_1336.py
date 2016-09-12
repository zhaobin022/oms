# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0008_auto_20160519_1146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='disk',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\xa4\xa7\xe5\xb0\x8f', blank=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='mem',
            field=models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe5\xa4\xa7\xe5\xb0\x8f', blank=True),
        ),
    ]
