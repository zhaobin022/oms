#_*_coding:utf-8_*_
__author__ = 'jieli'
from django.db import models
from user_center.models import UserProfile,UserGroup
import monitor


class App(models.Model):
    app_name =  models.CharField(max_length=30,unique=True)
    app_path = models.CharField(max_length=100,default='/xebest/release')
    svn_version = models.IntegerField(blank=True,null=True)
    svn_url = models.URLField(blank=True,null=True)
    description = models.CharField(max_length=20, verbose_name=u'应用描述',blank=True,null=True)
    def __unicode__(self):
        return self.app_name
    class Meta:
        verbose_name = '项目'
        verbose_name_plural = "项目"

class Server(models.Model):
    server_name = models.CharField(max_length=64, verbose_name=u'主机名',unique=True,blank=True,null=True)
    ipaddress = models.GenericIPAddressField(blank=True,null=True)
    ssh_port = models.SmallIntegerField(default=22)
    root_pwd = models.CharField(max_length=128,blank=True,null=True)
    new_pwd = models.CharField(max_length=128,blank=True,null=True)
    update_password_time = models.DateTimeField(null=True,blank=True)
    ssh_check_status = (
        (0, 'Successfull'),
        (1, 'Failed'),
    )
    ssh_check =  models.IntegerField(choices=ssh_check_status,blank=True,null=True,default=1)
    change_password_status = (
        (0, 'Successfull'),
        (1, 'Failed'),
    )
    change_password_tag = models.IntegerField(choices=change_password_status,blank=True,null=True,default=1)

    cpu_model = models.CharField(max_length=50, verbose_name=u'CPU型号',blank=True,null=True)
    cpu_count = models.PositiveSmallIntegerField(verbose_name=u'CPU数',blank=True,null=True)
    physical_cpu_count = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name=u'CPU物理个数')
    cpu_core_count = models.PositiveSmallIntegerField(blank=True,null=True,verbose_name=u'CPU内核数')
    ram_size = models.CharField(max_length=32, verbose_name='内存大小',blank=True,null=True)
    disk = models.CharField(max_length=32, verbose_name='硬盘大小',blank=True,null=True)
    raid = models.CharField(max_length=5, verbose_name='RAID级别',blank=True,null=True)
    macaddress = models.CharField(max_length=40, verbose_name=u'MAC地址',blank=True,null=True)
    os_release = models.CharField(max_length=255, verbose_name=u'操作系统',blank=True,null=True)
    virtual = models.CharField(max_length=20, verbose_name=u'是否为虚拟机',blank=True,null=True)
    idc_name = models.CharField(max_length=10, verbose_name=u'所属机房',blank=True,null=True)
    application = models.ForeignKey(App, verbose_name=u'应用',blank=True,null=True)
    status = models.BooleanField(default=False)
    remark = models.TextField(max_length=50, verbose_name=u'备注',blank=True,null=True)
    manufacturer = models.CharField(max_length=20, verbose_name=u'厂商',blank=True,null=True)
    sn = models.CharField(max_length=255, verbose_name=u'SN',unique=True,blank=True,null=True)
    os_type = models.CharField(max_length=30, verbose_name=u'操作系统类型',blank=True,null=True)
    os_distribution = models.CharField(max_length=30, verbose_name=u'系统分支',blank=True,null=True)
    templates = models.ManyToManyField('Template',blank=True) # A D E
    monitored_by_choices = (
        ('agent','Agent'),
        ('snmp','SNMP'),
        ('wget','WGET'),
    )
    monitored_by = models.CharField(u'监控方式',max_length=64,choices=monitored_by_choices,default='agent')
    status_choices= (
        (1,'Online'),
        (2,'Down'),
        (3,'Unreachable'),
        (4,'Offline'),
    )
    status = models.IntegerField(u'状态',choices=status_choices,default=1)

    def __unicode__(self):
        return self.server_name
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = "服务器"
        permissions =(('view_customer_list', u"可以查看客户列表"),
                      ('view_customer_info',u"可以查看客户详情"),
                      ('edit_own_customer_info',u"可以修改自己的客户信息"),
                      )

class SoftwareList(models.Model):
    software_name = models.CharField(max_length=20, verbose_name=u'软件名称')
    salt_state_module_name = models.CharField(max_length=20, verbose_name=u'salt模块名称')
    def __unicode__(self):
        return u'%s' % (self.software_name)

    class Meta:
        verbose_name = u'软件列表'
        verbose_name_plural = "软件列表"



class CmdbEventLog(models.Model):
    task_type_choices = (
        (0, 'Create Server Info'),
        (1, 'Update Server Info'),
    )
    task_type = models.SmallIntegerField(choices=task_type_choices,blank=True,null=True)
    server = models.ForeignKey(Server,blank=True,null=True)
    content = models.TextField()
    event_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)

    def __unicode__(self):
        return str(self.get_task_type_display()+self.server.server_name)

    class Meta:
        verbose_name = u'服务器配置更新事件'
        verbose_name_plural = "服务器配置更新事件"



class EventLog(models.Model):
    log_type_choice = (
        (0,'execute command'),
        (1,'update code'),
        (2,'install software'),
        (3,'update password'),
    )
    log_type = models.SmallIntegerField(choices=log_type_choice)
    user = models.ForeignKey(UserProfile)
    server = models.ForeignKey(Server)
    content = models.TextField()
    class Meta:
        verbose_name = u'事件日志'
        verbose_name_plural = "事件日志"
    def __unicode__(self):
        return self.get_log_type_display()




class ServerGroup(models.Model):
    group_name =  models.CharField(max_length=30,unique=True)
    servers  =  models.ManyToManyField(Server,blank=True)
    templates = models.ManyToManyField('Template',blank=True)
    description = models.TextField()
    def __unicode__(self):
        return self.group_name

    class Meta:
        verbose_name = u'服务器组'
        verbose_name_plural = "服务器组"


class OsUser(models.Model):
    username =  models.CharField(max_length=30,unique=True)
    server_group = models.ManyToManyField(ServerGroup)

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = u'操作系统用户'
        verbose_name_plural = "操作系统用户"

class JumpServerAudit(models.Model):
    happened_time = models.DateTimeField(auto_now_add=True)
    username =  models.CharField(max_length=30)
    content = models.TextField()
    def __unicode__(self):
        return str(self.id)

    class Meta:
        verbose_name = u'跳转Server审计'
        verbose_name_plural = "跳转Server审计"



class ServiceIndex(models.Model):
    name = models.CharField(max_length=64)
    key =models.CharField(max_length=64) #cpu , idle
    data_type_choices = (
        ('int',"int"),
        ('float',"float"),
        ('str',"string")
    )
    data_type = models.CharField('指标数据类型',max_length=32,choices=data_type_choices,default='int')
    memo = models.CharField("备注",max_length=128,blank=True,null=True)
    def __unicode__(self):
        return "%s.%s" %(self.name,self.key)

class Service(models.Model):
    name = models.CharField('服务名称',max_length=64,unique=True)
    interval = models.IntegerField('监控间隔',default=60)
    plugin_name = models.CharField('插件名',max_length=64,default='n/a')
    items = models.ManyToManyField('ServiceIndex',verbose_name="指标列表",blank=True)
    has_sub_service = models.BooleanField(default=False,help_text="如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡") #如果一个服务还有独立的子服务 ,选择这个,比如 网卡服务有多个独立的子网卡
    memo = models.CharField("备注",max_length=128,blank=True,null=True)

    def __unicode__(self):
        return self.name


class Template(models.Model):
    name = models.CharField('模版名称',max_length=64,unique=True)
    services = models.ManyToManyField(Service,verbose_name="服务列表")
    #services = models.ManyToManyField('Service2',verbose_name="服务列表")
    triggers = models.ManyToManyField('Trigger',verbose_name="触发器列表",blank=True)
    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'监控模版'
        verbose_name_plural = "监控模版"


class TriggerExpression(models.Model):
    #name = models.CharField("触发器表达式名称",max_length=64,blank=True,null=True)
    trigger = models.ForeignKey('Trigger',verbose_name="所属触发器")
    service = models.ForeignKey(Service,verbose_name="关联服务")
    service_index = models.ForeignKey(ServiceIndex,verbose_name="关联服务指标")
    specified_index_key = models.CharField(verbose_name="只监控专门指定的指标key",max_length=64,blank=True,null=True)
    operator_type_choices = (('eq','='),('lt','<'),('gt','>'))
    operator_type = models.CharField("运算符",choices=operator_type_choices,max_length=32)
    data_calc_type_choices = (
        ('avg','Average'),
        ('max','Max'),
        ('hit','Hit'),
        ('last','Last'),
    )
    data_calc_func= models.CharField("数据处理方式",choices=data_calc_type_choices,max_length=64)
    data_calc_args = models.CharField("函数传入参数",help_text="若是多个参数,则用,号分开,第一个值是时间",max_length=64)
    threshold = models.IntegerField("阈值")


    logic_type_choices = (('or','OR'),('and','AND'))
    logic_type = models.CharField("与一个条件的逻辑关系",choices=logic_type_choices,max_length=32,blank=True,null=True)
    #next_condition = models.ForeignKey('self',verbose_name="右边条件",blank=True,null=True,related_name='right_sibling_condition' )
    def __unicode__(self):
        return "%s %s(%s(%s))" %(self.service_index,self.operator_type,self.data_calc_func,self.data_calc_args)
    class Meta:
        pass #unique_together = ('trigger_id','service')

class Trigger(models.Model):
    name = models.CharField('触发器名称',max_length=64)
    #expressions= models.TextField("表达式")
    severity_choices = (
        (1,'Information'),
        (2,'Warning'),
        (3,'Average'),
        (4,'High'),
        (5,'Diaster'),
    )
    #expressions = models.ManyToManyField(TriggerExpression,verbose_name="条件表达式")
    severity = models.IntegerField('告警级别',choices=severity_choices)
    enabled = models.BooleanField(default=True)
    memo = models.TextField("备注",blank=True,null=True)

    def __unicode__(self):
        return "<serice:%s, severity:%s>" %(self.name,self.get_severity_display())



class Action(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    host_groups = models.ManyToManyField(ServerGroup,blank=True)
    hosts = models.ManyToManyField(Server,blank=True)

    conditions = models.TextField('告警条件')
    interval = models.IntegerField('告警间隔(s)',default=300)
    operations = models.ManyToManyField('ActionOperation')

    recover_notice = models.BooleanField('故障恢复后发送通知消息',default=True)
    recover_subject = models.CharField(max_length=128,blank=True,null=True)
    recover_message = models.TextField(blank=True,null=True)
    user = models.ManyToManyField(UserProfile,blank=True)
    user_group = models.ManyToManyField(UserGroup,blank=True)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class ActionOperation(models.Model):
    name =  models.CharField(max_length=64)
    step = models.SmallIntegerField("第n次告警",default=1)
    medis_type = models.ManyToManyField('Media',blank=True)
    #notifiers= models.ManyToManyField(host_models.UserProfile,verbose_name="通知对象",blank=True)
    def __unicode__(self):
        return self.name


class Maintenance(models.Model):
    name =  models.CharField(max_length=64,unique=True)
    hosts = models.ManyToManyField(Server,blank=True)
    host_groups = models.ManyToManyField(ServerGroup,blank=True)
    content = models.TextField("维护内容")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __unicode__(self):
        return self.name

class Media(models.Model):
    media_name = models.CharField(max_length=64,unique=True)
    media_type_choices = (
        ('email','Email'),
        ('sms','SMS'),
        ('script','RunScript'),
    )
    media_type = models.CharField("动作类型",choices=media_type_choices,default='email',max_length=64)
    stmp_server = models.CharField(max_length=255,blank=True,null=True)
    email_user = models.CharField(max_length=64,blank=True,null=True)
    email_password = models.CharField(max_length=64,blank=True,null=True)
    gsm_moden = models.CharField(max_length=255,blank=True,null=True)
    script_path = models.CharField(max_length=255,blank=True,null=True)

    def __unicode__(self):
        return self.media_name








