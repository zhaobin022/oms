# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0014_auto_20160520_1045'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='ip',
            new_name='ipaddress',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='os',
            new_name='os_release',
        ),
        migrations.RenameField(
            model_name='server',
            old_name='mem',
            new_name='ram_size',
        ),
        migrations.RemoveField(
            model_name='server',
            name='productname',
        ),
        migrations.AddField(
            model_name='server',
            name='os_distribution',
            field=models.CharField(max_length=30, null=True, verbose_name='\u7cfb\u7edf\u5206\u652f', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='os_type',
            field=models.CharField(max_length=30, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7c7b\u578b', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='sn',
            field=models.CharField(max_length=255, unique=True, null=True, verbose_name='SN', blank=True),
        ),
    ]
