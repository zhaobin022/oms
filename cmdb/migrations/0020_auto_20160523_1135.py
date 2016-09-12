# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0019_auto_20160523_1122'),
    ]

    operations = [
        migrations.RenameField(
            model_name='app',
            old_name='svn_number',
            new_name='svn_version',
        ),
    ]
