# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0031_auto_20160527_1117'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jumpserveraudit',
            options={'verbose_name': '\u8df3\u8f6cServer\u5ba1\u8ba1', 'verbose_name_plural': '\u8df3\u8f6cServer\u5ba1\u8ba1'},
        ),
        migrations.AlterModelOptions(
            name='osuser',
            options={'verbose_name': '\u64cd\u4f5c\u7cfb\u7edf\u7528\u6237', 'verbose_name_plural': '\u64cd\u4f5c\u7cfb\u7edf\u7528\u6237'},
        ),
        migrations.AlterModelOptions(
            name='servergroup',
            options={'verbose_name': '\u670d\u52a1\u5668\u7ec4', 'verbose_name_plural': '\u670d\u52a1\u5668\u7ec4'},
        ),
    ]
