# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0018_app_svn_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='app',
            name='upload_path',
        ),
        migrations.AlterField(
            model_name='app',
            name='app_path',
            field=models.CharField(default=b'/xebest/release', max_length=100),
        ),
    ]
