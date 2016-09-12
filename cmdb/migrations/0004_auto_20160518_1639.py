# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20160518_1515'),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(unique=True, max_length=30)),
                ('upload_path', models.CharField(max_length=100)),
                ('app_path', models.CharField(default=b'release', max_length=100)),
                ('backup_path', models.CharField(max_length=100)),
                ('start_script_path', models.CharField(default=b'/xebest/tomcat/bin/startup.sh', max_length=100)),
                ('stop_script_path', models.CharField(default=b'killall -9 java', max_length=100)),
                ('publish_date', models.DateTimeField(null=True, blank=True)),
                ('war_file', models.NullBooleanField()),
                ('war_file_path', models.CharField(max_length=100, null=True, blank=True)),
                ('rollback_status', models.CharField(max_length=30, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
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
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task_type', models.IntegerField(null=True, choices=[(0, b'Publish'), (1, b'Backup'), (2, b'Rollback'), (3, b'Startup'), (4, b'Shutdown'), (5, b'DeleteBackup'), (6, b'UnzipWar'), (7, b'CheckApp')])),
                ('total_count', models.IntegerField(default=0)),
                ('complete_count', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='asset',
            name='admin',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='business_unit',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='contract',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='idc',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='manufactory',
        ),
        migrations.RemoveField(
            model_name='asset',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='businessunit',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='businessunit',
            name='parent_unit',
        ),
        migrations.RemoveField(
            model_name='cpu',
            name='asset',
        ),
        migrations.AlterUniqueTogether(
            name='disk',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='disk',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='eventlog',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='eventlog',
            name='user',
        ),
        migrations.RemoveField(
            model_name='networkdevice',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='networkdevice',
            name='firmware',
        ),
        migrations.RemoveField(
            model_name='newassetapprovalzone',
            name='approved_by',
        ),
        migrations.RemoveField(
            model_name='nic',
            name='asset',
        ),
        migrations.AlterUniqueTogether(
            name='raidadaptor',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='raidadaptor',
            name='asset',
        ),
        migrations.AlterUniqueTogether(
            name='ram',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='ram',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='creater',
        ),
        migrations.RemoveField(
            model_name='server',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='server',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='server',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='server',
            name='hosted_on',
        ),
        migrations.RemoveField(
            model_name='server',
            name='management_ip',
        ),
        migrations.RemoveField(
            model_name='server',
            name='manufactory',
        ),
        migrations.RemoveField(
            model_name='server',
            name='model',
        ),
        migrations.RemoveField(
            model_name='server',
            name='nic',
        ),
        migrations.RemoveField(
            model_name='server',
            name='os_distribution',
        ),
        migrations.RemoveField(
            model_name='server',
            name='os_release',
        ),
        migrations.RemoveField(
            model_name='server',
            name='os_type',
        ),
        migrations.RemoveField(
            model_name='server',
            name='physical_disk_driver',
        ),
        migrations.RemoveField(
            model_name='server',
            name='raid_adaptor',
        ),
        migrations.RemoveField(
            model_name='server',
            name='raid_type',
        ),
        migrations.RemoveField(
            model_name='server',
            name='ram',
        ),
        migrations.RemoveField(
            model_name='server',
            name='ram_capacity',
        ),
        migrations.RemoveField(
            model_name='server',
            name='sn',
        ),
        migrations.RemoveField(
            model_name='server',
            name='update_date',
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_groups',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u7269\u7406\u6838\u6570', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_model',
            field=models.CharField(max_length=50, null=True, verbose_name='CPU\u578b\u53f7', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='cpu_nums',
            field=models.PositiveSmallIntegerField(null=True, verbose_name='CPU\u7ebf\u7a0b\u6570', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='disk',
            field=models.CharField(max_length=5, null=True, verbose_name=b'\xe7\xa1\xac\xe7\x9b\x98\xe5\xa4\xa7\xe5\xb0\x8f', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='hostname',
            field=models.CharField(max_length=30, unique=True, null=True, verbose_name='\u4e3b\u673a\u540d', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='idc_name',
            field=models.CharField(max_length=10, null=True, verbose_name='\u6240\u5c5e\u673a\u623f', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='ip',
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='macaddress',
            field=models.CharField(max_length=40, null=True, verbose_name='MAC\u5730\u5740', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='mem',
            field=models.CharField(max_length=5, null=True, verbose_name=b'\xe5\x86\x85\xe5\xad\x98\xe5\xa4\xa7\xe5\xb0\x8f', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='os',
            field=models.CharField(max_length=20, null=True, verbose_name='\u64cd\u4f5c\u7cfb\u7edf', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='raid',
            field=models.CharField(max_length=5, null=True, verbose_name=b'RAID\xe7\xba\xa7\xe5\x88\xab', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='remark',
            field=models.TextField(max_length=50, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='root_pwd',
            field=models.CharField(max_length=128, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='server_name',
            field=models.CharField(max_length=64, unique=True, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='server',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='server',
            name='virtual',
            field=models.CharField(max_length=20, null=True, verbose_name='\u662f\u5426\u4e3a\u865a\u62df\u673a', blank=True),
        ),
        migrations.DeleteModel(
            name='Asset',
        ),
        migrations.DeleteModel(
            name='BusinessUnit',
        ),
        migrations.DeleteModel(
            name='Contract',
        ),
        migrations.DeleteModel(
            name='CPU',
        ),
        migrations.DeleteModel(
            name='Disk',
        ),
        migrations.DeleteModel(
            name='EventLog',
        ),
        migrations.DeleteModel(
            name='IDC',
        ),
        migrations.DeleteModel(
            name='Manufactory',
        ),
        migrations.DeleteModel(
            name='NetworkDevice',
        ),
        migrations.DeleteModel(
            name='NewAssetApprovalZone',
        ),
        migrations.DeleteModel(
            name='NIC',
        ),
        migrations.DeleteModel(
            name='RaidAdaptor',
        ),
        migrations.DeleteModel(
            name='RAM',
        ),
        migrations.DeleteModel(
            name='Software',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AddField(
            model_name='app',
            name='task',
            field=models.ForeignKey(blank=True, to='cmdb.TaskLog', null=True),
        ),
        migrations.AddField(
            model_name='server',
            name='application',
            field=models.ForeignKey(verbose_name='\u5e94\u7528', blank=True, to='cmdb.App', null=True),
        ),
    ]
