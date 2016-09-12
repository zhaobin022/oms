# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0015_auto_20160520_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='os_release',
            field=models.CharField(max_length=255, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf', blank=True),
        ),
    ]
