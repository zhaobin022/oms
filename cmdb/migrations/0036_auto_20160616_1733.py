# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_center', '0009_userprofile_phone'),
        ('cmdb', '0035_actionoperation_script_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='action',
            name='user_group',
            field=models.ManyToManyField(to='user_center.UserGroup'),
        ),
    ]
