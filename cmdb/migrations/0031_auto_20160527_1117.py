# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0030_auto_20160527_1024'),
    ]

    operations = [
        migrations.CreateModel(
            name='JumpServerAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('happened_time', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=30)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='OsUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ServerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(unique=True, max_length=30)),
                ('description', models.TextField()),
                ('servers', models.ManyToManyField(to='cmdb.Server')),
            ],
        ),
        migrations.AddField(
            model_name='osuser',
            name='server_group',
            field=models.ManyToManyField(to='cmdb.ServerGroup'),
        ),
    ]
