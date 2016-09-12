# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
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
            ],
        ),
        migrations.CreateModel(
            name='ActionOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('step', models.SmallIntegerField(default=1, verbose_name=b'\xe7\xac\xacn\xe6\xac\xa1\xe5\x91\x8a\xe8\xad\xa6')),
            ],
        ),
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(unique=True, max_length=30)),
                ('app_path', models.CharField(default=b'/xebest/release', max_length=100)),
                ('svn_version', models.IntegerField(null=True, blank=True)),
                ('svn_url', models.URLField(null=True, blank=True)),
                ('description', models.CharField(max_length=20, null=True, verbose_name='\u5e94\u7528\u63cf\u8ff0', blank=True)),
            ],
            options={
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
        ),
        migrations.CreateModel(
            name='CmdbEventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_type', models.SmallIntegerField(blank=True, null=True, choices=[(0, b'Create Server Info'), (1, b'Update Server Info')])),
                ('content', models.TextField()),
                ('event_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668\u914d\u7f6e\u66f4\u65b0\u4e8b\u4ef6',
                'verbose_name_plural': '\u670d\u52a1\u5668\u914d\u7f6e\u66f4\u65b0\u4e8b\u4ef6',
            },
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('log_type', models.SmallIntegerField(choices=[(0, b'execute command'), (1, b'update code'), (2, b'install software'), (3, b'update password')])),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': '\u4e8b\u4ef6\u65e5\u5fd7',
                'verbose_name_plural': '\u4e8b\u4ef6\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='JumpServerAudit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('happened_time', models.DateTimeField(auto_now_add=True)),
                ('username', models.CharField(max_length=30)),
                ('content', models.TextField()),
            ],
            options={
                'verbose_name': '\u8df3\u8f6cServer\u5ba1\u8ba1',
                'verbose_name_plural': '\u8df3\u8f6cServer\u5ba1\u8ba1',
            },
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('content', models.TextField(verbose_name=b'\xe7\xbb\xb4\xe6\x8a\xa4\xe5\x86\x85\xe5\xae\xb9')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('media_name', models.CharField(unique=True, max_length=64)),
                ('media_type', models.CharField(default=b'email', max_length=64, verbose_name=b'\xe5\x8a\xa8\xe4\xbd\x9c\xe7\xb1\xbb\xe5\x9e\x8b', choices=[(b'email', b'Email'), (b'sms', b'SMS'), (b'script', b'RunScript')])),
                ('stmp_server', models.CharField(max_length=255, null=True, blank=True)),
                ('email_user', models.CharField(max_length=64, null=True, blank=True)),
                ('email_password', models.CharField(max_length=64, null=True, blank=True)),
                ('gsm_moden', models.CharField(max_length=255, null=True, blank=True)),
                ('script_path', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OsUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=30)),
            ],
            options={
                'verbose_name': '\u64cd\u4f5c\u7cfb\u7edf\u7528\u6237',
                'verbose_name_plural': '\u64cd\u4f5c\u7cfb\u7edf\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('server_name', models.CharField(max_length=64, unique=True, null=True, verbose_name='\u4e3b\u673a\u540d', blank=True)),
                ('ipaddress', models.GenericIPAddressField(null=True, blank=True)),
                ('ssh_port', models.SmallIntegerField(default=22)),
                ('root_pwd', models.CharField(max_length=128, null=True, blank=True)),
                ('new_pwd', models.CharField(max_length=128, null=True, blank=True)),
                ('update_password_time', models.DateTimeField(null=True, blank=True)),
                ('ssh_check', models.IntegerField(default=1, null=True, blank=True, choices=[(0, b'Successfull'), (1, b'Failed')])),
                ('change_password_tag', models.IntegerField(default=1, null=True, blank=True, choices=[(0, b'Successfull'), (1, b'Failed')])),
                ('cpu_model', models.CharField(max_length=50, null=True, verbose_name='CPU\u578b\u53f7', blank=True)),
                ('cpu_count', models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u6570', blank=True)),
                ('physical_cpu_count', models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u7269\u7406\u4e2a\u6570', blank=True)),
                ('cpu_core_count', models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u5185\u6838\u6570', blank=True)),
                ('ram_size', models.CharField(max_length=32, null=True, verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe5\xa4\xa7\xe5\xb0\x8f', blank=True)),
                ('disk', models.CharField(max_length=32, null=True, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\xa4\xa7\xe5\xb0\x8f', blank=True)),
                ('raid', models.CharField(max_length=5, null=True, verbose_name=b'RAID\xe7\xba\xa7\xe5\x88\xab', blank=True)),
                ('macaddress', models.CharField(max_length=40, null=True, verbose_name='MAC\u5730\u5740', blank=True)),
                ('os_release', models.CharField(max_length=255, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf', blank=True)),
                ('virtual', models.CharField(max_length=20, null=True, verbose_name='\u662f\u5426\u4e3a\u865a\u62df\u673a', blank=True)),
                ('idc_name', models.CharField(max_length=10, null=True, verbose_name='\u6240\u5c5e\u673a\u623f', blank=True)),
                ('remark', models.TextField(max_length=50, null=True, verbose_name='\u5907\u6ce8', blank=True)),
                ('manufacturer', models.CharField(max_length=20, null=True, verbose_name='\u5382\u5546', blank=True)),
                ('sn', models.CharField(max_length=255, unique=True, null=True, verbose_name='SN', blank=True)),
                ('os_type', models.CharField(max_length=30, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf\u7c7b\u578b', blank=True)),
                ('os_distribution', models.CharField(max_length=30, null=True, verbose_name='\u7cfb\u7edf\u5206\u652f', blank=True)),
                ('monitored_by', models.CharField(default=b'agent', max_length=64, verbose_name='\u76d1\u63a7\u65b9\u5f0f', choices=[(b'agent', b'Agent'), (b'snmp', b'SNMP'), (b'wget', b'WGET')])),
                ('status', models.IntegerField(default=1, verbose_name='\u72b6\u6001', choices=[(1, b'Online'), (2, b'Down'), (3, b'Unreachable'), (4, b'Offline')])),
                ('application', models.ForeignKey(verbose_name='\u5e94\u7528', blank=True, to='cmdb.App', null=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668',
                'verbose_name_plural': '\u670d\u52a1\u5668',
                'permissions': (('view_customer_list', '\u53ef\u4ee5\u67e5\u770b\u5ba2\u6237\u5217\u8868'), ('view_customer_info', '\u53ef\u4ee5\u67e5\u770b\u5ba2\u6237\u8be6\u60c5'), ('edit_own_customer_info', '\u53ef\u4ee5\u4fee\u6539\u81ea\u5df1\u7684\u5ba2\u6237\u4fe1\u606f')),
            },
        ),
        migrations.CreateModel(
            name='ServerGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(unique=True, max_length=30)),
                ('description', models.TextField()),
                ('servers', models.ManyToManyField(to='cmdb.Server', blank=True)),
            ],
            options={
                'verbose_name': '\u670d\u52a1\u5668\u7ec4',
                'verbose_name_plural': '\u670d\u52a1\u5668\u7ec4',
            },
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
            name='SoftwareList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('software_name', models.CharField(max_length=20, verbose_name='\u8f6f\u4ef6\u540d\u79f0')),
                ('salt_state_module_name', models.CharField(max_length=20, verbose_name='salt\u6a21\u5757\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u8f6f\u4ef6\u5217\u8868',
                'verbose_name_plural': '\u8f6f\u4ef6\u5217\u8868',
            },
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64, verbose_name=b'\xe6\xa8\xa1\xe7\x89\x88\xe5\x90\x8d\xe7\xa7\xb0')),
                ('services', models.ManyToManyField(to='cmdb.Service', verbose_name=b'\xe6\x9c\x8d\xe5\x8a\xa1\xe5\x88\x97\xe8\xa1\xa8')),
            ],
            options={
                'verbose_name': '\u76d1\u63a7\u6a21\u7248',
                'verbose_name_plural': '\u76d1\u63a7\u6a21\u7248',
            },
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
            model_name='servergroup',
            name='templates',
            field=models.ManyToManyField(to='cmdb.Template', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='templates',
            field=models.ManyToManyField(to='cmdb.Template', blank=True),
        ),
        migrations.AddField(
            model_name='osuser',
            name='server_group',
            field=models.ManyToManyField(to='cmdb.ServerGroup'),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='host_groups',
            field=models.ManyToManyField(to='cmdb.ServerGroup', blank=True),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='hosts',
            field=models.ManyToManyField(to='cmdb.Server', blank=True),
        ),
        migrations.AddField(
            model_name='eventlog',
            name='server',
            field=models.ForeignKey(to='cmdb.Server'),
        ),
    ]
