# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usergroup',
            options={'verbose_name': '\u7cfb\u7edf\u7ec4', 'verbose_name_plural': '\u7cfb\u7edf\u7ec4'},
        ),
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name': '\u7cfb\u7edf\u7528\u6237', 'verbose_name_plural': '\u7cfb\u7edf\u7528\u6237'},
        ),
    ]
