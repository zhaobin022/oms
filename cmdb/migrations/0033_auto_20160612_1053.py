# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0032_auto_20160527_1121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('conditions', models.TextField(verbose_name=b'\xe5\x91\x8a\xe8\xad\xa6\xe6\x9d\xa1\xe4\xbb\xb6')),
                ('interval', models.IntegerField(default=300, verbose_name=b'\xe5\x91\x8a\xe8\xad\xa6\xe9\x97\xb4\xe9\x9a\x94(s)')),
                ('recover_notice', models.BooleanField(default=True, verbose_name=b'\xe6\x95\x85\xe9\x9a\x9c\xe6\x81\xa2\xe5\xa4\x8d\xe5\x90\x8e\xe5\x8f\x91\xe9\x80\x81\xe9\x80\x9a\xe7\x9f\xa5\xe6\xb6\x88\xe6\x81\xaf')),
                ('recover_subject', models.CharField(max_length=128, null=True, blank=True)),
                ('recover_message', models.TextField(null=True, blank=True)),
                ('enabled', models.BooleanField(default=True)),
                ('host_groups', models.ManyToManyField(to='cmdb.ServerGroup', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ActionOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('step', models.SmallIntegerField(default=1, verbose_name=b'\xe7\xac\xacn\xe6\xac\xa1\xe5\x91\x8a\xe8\xad\xa6')),
                ('action_type', models.CharField(default=b'email', max_length=64, verbose_name=b'\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'email', b'Email'), (b'sms', b'SMS'), (b'script', b'RunScript')])),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('content', models.TextField(verbose_name=b'\xe7\xbb\xb4\xe6\x8a\xa4\xe5\x86\x85\xe5\xae\xb9')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('host_groups', models.ManyToManyField(to='cmdb.ServerGroup', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x90\x8d\xe7\xa7\xb0')),
                ('interval', models.IntegerField(default=60, verbose_name=b'\xe7\x9b\x91\xe6\x8e\xa7\xe9\x97\xb4\xe9\x9a\x94')),
                ('plugin_name', models.CharField(default=b'n/a', max_length=64, verbose_name=b'\xe6\x8f\x92\xe4\xbb\xb6\xe5\x90\x8d')),
                ('has_sub_service', models.BooleanField(default=False, help_text=b'\xe5\xa6\x82\xe6\x9e\x9c\xe4\xb8\x80\xe4\xb8\xaa\xe6\x9c\x8d\xe5\x8a\xa1\xe8\xbf\x98\xe6\x9c\x89\xe7\x8b\xac\xe7\xab\x8b\xe7\x9a\x84\xe5\xad\x90\xe6\x9c\x8d\xe5\x8a\xa1 ,\xe9\x80\x89\xe6\x8b\xa9\xe8\xbf\x99\xe4\xb8\xaa,\xe6\xaf\x94\xe5\xa6\x82 \xe7\xbd\x91\xe5\x8d\xa1\xe6\x9c\x8d\xe5\x8a\xa1\xe6\x9c\x89\xe5\xa4\x9a\xe4\xb8\xaa\xe7\x8b\xac\xe7\xab\x8b\xe7\x9a\x84\xe5\xad\x90\xe7\xbd\x91\xe5\x8d\xa1')),
                ('memo', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceIndex',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('key', models.CharField(max_length=64)),
                ('data_type', models.CharField(default=b'int', max_length=32, verbose_name=b'\xe6\x8c\x87\xe6\xa0\x87\xe6\x95\xb0\xe6\x8d\xae\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'int', b'int'), (b'float', b'float'), (b'str', b'string')])),
                ('memo', models.CharField(max_length=128, null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name=b'\xe6\xa8\xa1\xe7\x89\x88\xe5\x90\x8d\xe7\xa7\xb0')),
                ('services', models.ManyToManyField(to='cmdb.Service', verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8')),
            ],
        ),
        migrations.CreateModel(
            name='Trigger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name=b'\xe8\xa7\xa6\xe5\x8f\x91\xe5\x99\xa8\xe5\x90\x8d\xe7\xa7\xb0')),
                ('severity', models.IntegerField(verbose_name=b'\xe5\x91\x8a\xe8\xad\xa6\xe7\xba\xa7\xe5\x88\xab', choices=[(1, b'Information'), (2, b'Warning'), (3, b'Average'), (4, b'High'), (5, b'Diaster')])),
                ('enabled', models.BooleanField(default=True)),
                ('memo', models.TextField(null=True, verbose_name=b'\xe5\xa4\x87\xe6\xb3\xa8', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TriggerExpression',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('specified_index_key', models.CharField(max_length=64, null=True, verbose_name=b'\xe5\x8f\xaa\xe7\x9b\x91\xe6\x8e\xa7\xe4\xb8\x93\xe9\x97\xa8\xe6\x8c\x87\xe5\xae\x9a\xe7\x9a\x84\xe6\x8c\x87\xe6\xa0\x87key', blank=True)),
                ('operator_type', models.CharField(max_length=32, verbose_name=b'\xe8\xbf\x90\xe7\xae\x97\xe7\xac\xa6', choices=[(b'eq', b'='), (b'lt', b'<'), (b'gt', b'>')])),
                ('data_calc_func', models.CharField(max_length=64, verbose_name=b'\xe6\x95\xb0\xe6\x8d\xae\xe5\xa4\x84\xe7\x90\x86\xe6\x96\xb9\xe5\xbc\x8f', choices=[(b'avg', b'Average'), (b'max', b'Max'), (b'hit', b'Hit'), (b'last', b'Last')])),
                ('data_calc_args', models.CharField(help_text=b'\xe8\x8b\xa5\xe6\x98\xaf\xe5\xa4\x9a\xe4\xb8\xaa\xe5\x8f\x82\xe6\x95\xb0,\xe5\x88\x99\xe7\x94\xa8,\xe5\x8f\xb7\xe5\x88\x86\xe5\xbc\x80,\xe7\xac\xac\xe4\xb8\x80\xe4\xb8\xaa\xe5\x80\xbc\xe6\x98\xaf\xe6\x97\xb6\xe9\x97\xb4', max_length=64, verbose_name=b'\xe5\x87\xbd\xe6\x95\xb0\xe4\xbc\xa0\xe5\x85\xa5\xe5\x8f\x82\xe6\x95\xb0')),
                ('threshold', models.IntegerField(verbose_name=b'\xe9\x98\x88\xe5\x80\xbc')),
                ('logic_type', models.CharField(blank=True, max_length=32, null=True, verbose_name=b'\xe4\xb8\x8e\xe4\xb8\x80\xe4\xb8\xaa\xe6\x9d\xa1\xe4\xbb\xb6\xe7\x9a\x84\xe9\x80\xbb\xe8\xbe\x91\xe5\x85\xb3\xe7\xb3\xbb', choices=[(b'or', b'OR'), (b'and', b'AND')])),
                ('service', models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe6\x9c\x8d\xe5\x8a\xa1', to='cmdb.Service')),
                ('service_index', models.ForeignKey(verbose_name=b'\xe5\x85\xb3\xe8\x81\x94\xe6\x9c\x8d\xe5\x8a\xa1\xe6\x8c\x87\xe6\xa0\x87', to='cmdb.ServiceIndex')),
                ('trigger', models.ForeignKey(verbose_name=b'\xe6\x89\x80\xe5\xb1\x9e\xe8\xa7\xa6\xe5\x8f\x91\xe5\x99\xa8', to='cmdb.Trigger')),
            ],
        ),
        migrations.AddField(
            model_name='server',
            name='monitored_by',
            field=models.CharField(default=b'agent', max_length=64, verbose_name='\u76d1\u63a7\u65b9\u5f0f', choices=[(b'agent', b'Agent'), (b'snmp', b'SNMP'), (b'wget', b'WGET')]),
        ),
        migrations.AlterField(
            model_name='server',
            name='status',
            field=models.IntegerField(default=1, verbose_name='\u72b6\u6001', choices=[(1, b'Online'), (2, b'Down'), (3, b'Unreachable'), (4, b'Offline')]),
        ),
        migrations.AddField(
            model_name='template',
            name='triggers',
            field=models.ManyToManyField(to='cmdb.Trigger', verbose_name=b'\xe8\xa7\xa6\xe5\x8f\x91\xe5\x99\xa8\xe5\x88\x97\xe8\xa1\xa8', blank=True),
        ),
        migrations.AddField(
            model_name='service',
            name='items',
            field=models.ManyToManyField(to='cmdb.ServiceIndex', verbose_name=b'\xe6\x8c\x87\xe6\xa0\x87\xe5\x88\x97\xe8\xa1\xa8', blank=True),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='hosts',
            field=models.ManyToManyField(to='cmdb.Server', blank=True),
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
            model_name='server',
            name='templates',
            field=models.ManyToManyField(to='cmdb.Template', blank=True),
        ),
        migrations.AddField(
            model_name='servergroup',
            name='templates',
            field=models.ManyToManyField(to='cmdb.Template', blank=True),
        ),
    ]
