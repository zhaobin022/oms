# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0006_server_manufacturer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='server',
            name='hostname',
        ),
        migrations.AlterField(
            model_name='server',
            name='server_name',
            field=models.CharField(max_length=64, unique=True, null=True, verbose_name='\u4e3b\u673a\u540d', blank=True),
        ),
    ]
