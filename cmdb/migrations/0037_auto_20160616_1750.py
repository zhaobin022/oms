# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0036_auto_20160616_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='action',
            name='user_group',
            field=models.ManyToManyField(to='user_center.UserGroup', blank=True),
        ),
    ]
