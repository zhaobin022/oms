# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0021_server_application'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='description',
            field=models.CharField(max_length=20, null=True, verbose_name='\u5e94\u7528\u63cf\u8ff0', blank=True),
        ),
    ]
