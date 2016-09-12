# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0025_server_ssh_port'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='svn_url',
            field=models.URLField(null=True, blank=True),
        ),
    ]
