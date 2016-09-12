# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0013_server_cpu_core_count'),
    ]

    operations = [
        migrations.RenameField(
            model_name='server',
            old_name='cpu_nums',
            new_name='cpu_count',
        ),
    ]
