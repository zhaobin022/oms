# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_center', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cmdb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cmdbeventlog',
            name='server',
            field=models.ForeignKey(blank=True, to='cmdb.Server', null=True),
        ),
        migrations.AddField(
            model_name='actionoperation',
            name='medis_type',
            field=models.ManyToManyField(to='cmdb.Media', blank=True),
        ),
        migrations.AddField(
            model_name='action',
            name='host_groups',
            field=models.ManyToManyField(to='cmdb.ServerGroup', blank=True),
        ),
        migrations.AddField(
            model_name='action',
            name='hosts',
            field=models.ManyToManyField(to='cmdb.Server', blank=True),
        ),
        migrations.AddField(
            model_name='action',
            name='operations',
            field=models.ManyToManyField(to='cmdb.ActionOperation'),
        ),
        migrations.AddField(
            model_name='action',
            name='user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='action',
            name='user_group',
            field=models.ManyToManyField(to='user_center.UserGroup', blank=True),
        ),
    ]
