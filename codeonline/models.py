#-*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User
from cmdb.models import UserProfile
from cmdb.models import App


class OnlineRequest(models.Model):
    request_time = models.DateTimeField(auto_now_add=True,verbose_name=u'申请时间')
    developer = models.ManyToManyField(UserProfile,verbose_name=u'开发人员',related_name='developer')
    require_side = models.ManyToManyField(UserProfile,verbose_name=u'需求方',related_name='require_side')
    function_type_choices = (
        (1,'app'),
        (2,'bug'),
        (3,'both'),
    )
    function_type =  models.IntegerField(choices=function_type_choices,verbose_name=u'功能类型',blank=True,null=True)
    test_result_tag = models.BooleanField(default=False,verbose_name=u'测试结果')
    version_tag = models.CharField(max_length=30, verbose_name=u'版本标识',blank=True)
    online_function = models.TextField(verbose_name=u'上线功能')
    app = models.ManyToManyField(App,verbose_name=u'上线项目')
    online_files = models.TextField(verbose_name=u'上线文件')
    online_operation_choice = (
        (1,u'重启缓存'),
        (2,u'定时任务'),
    )
    online_operation = models.IntegerField(blank=True,null=True,choices=online_operation_choice,verbose_name=u'发版是否需要如下操作')
    assign_developer_leader = models.ForeignKey(UserProfile,blank=True,null=True,verbose_name=u'分配开发组')
    developer_fun_confirm_before_online = models.ForeignKey(UserProfile,blank=True,null=True,verbose_name=u'开发人员功能确认',related_name='developer_fun_confirm_before_online')
    technical_man_fun_confirm_online = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'技术经理功能确认',related_name='technical_man_fun_confirm_online')
    product_man_confirm_before_online = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'产品经理上线前确认',related_name='product_man_confirm_before_online')
    test_confirm_before_online = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'测试人员上线前功能确认',related_name='test_confirm_before_online')
    white_box_test = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'百盒功能确认',related_name='white_box_test')
    maintenance_persion_comfirm = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'运维人员确认',related_name='maintenance_persion_comfirm')
    maintenance_manager_comfirm = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'运维经理确认',related_name='maintenance_manager_comfirm')
    test_confirm_after_online = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'测试人员上线后功能确认',related_name='test_confirm_after_online')
    product_man_confirm_after_online = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'产品上线后功能确认',related_name='product_man_confirm_after_online')
    test_man_confirm_after_online = models.ManyToManyField(UserProfile,blank=True,verbose_name=u'测试经理上线后功能确认',related_name='test_man_confirm_after_online')
    cto_confirm = models.ForeignKey(UserProfile,blank=True,verbose_name=u'CTO上线后功能确认',related_name='cto_confirm',null=True)
    suggest_update_time = models.DateTimeField(blank=True,null=True,verbose_name=u'建议上线时间')
    update_code_time = models.DateTimeField(blank=True,null=True,verbose_name=u'代码上线时间')
    online_request_status_choice = (
        (1,u'产品经理已提交申请'),
        (2,u'上线前开发组长已确认'),
        (3,u'上线前测试经理已确认'),
        (4,u'上线前技术经理已确认'),
        (5,u'运维上线已确认'),
        (6,u'运维经理上线已确认'),
        (7,u'测试经理上线后已确认'),
        (8,u'产品经理上线后已确认(完结)'),
    )
    online_request_status = models.IntegerField(blank=True,null=True,choices=online_request_status_choice,verbose_name=u'流程状态')

    def __unicode__(self):
            return str(self.id)+":"+self.online_function

    class Meta:
        verbose_name = u'上线流程表'
        verbose_name_plural = "上线流程表"

