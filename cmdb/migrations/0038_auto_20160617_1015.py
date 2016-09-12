# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0037_auto_20160616_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media_name', models.CharField(unique=True, max_length=64)),
                ('media_type', models.CharField(default=b'email', max_length=64, verbose_name=b'\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'email', b'Email'), (b'sms', b'SMS'), (b'script', b'RunScript')])),
                ('stmp_server', models.CharField(max_length=255, null=True, blank=True)),
                ('gsm_moden', models.CharField(max_length=255, null=True, blank=True)),
                ('script_path', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='actionoperation',
            name='action_type',
        ),
        migrations.RemoveField(
            model_name='actionoperation',
            name='script_path',
        ),
        migrations.AddField(
            model_name='actionoperation',
            name='medis_type',
            field=models.ManyToManyField(to='cmdb.Media', blank=True),
        ),
    ]
