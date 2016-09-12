
from django.contrib import admin
# from models import App
from models import Server
from models import SoftwareList
from models import CmdbEventLog
from models import App
from models import EventLog
from models import ServerGroup
from models import OsUser
from models import JumpServerAudit
from models import Template
from models import Service
from models import ServiceIndex
from models import Trigger
from models import TriggerExpression
from models import Action
from models import ActionOperation
from models import Media
from models import Maintenance


from django import forms
# admin.site.register(App)

class CmdbEventLogAdmin(admin.ModelAdmin):
    list_display = ('task_type', 'server','content','event_time')
    readonly_fields = ('task_type','server','content','event_time')
    list_filter = ('task_type','event_time','server__server_name',)

class EventLogAdmin(admin.ModelAdmin):
    def log_type(self,obj):
        return obj.get_log_type_display


    def username(self,obj):
        return obj.user.alias

    def server_name(self,obj):
        return obj.server.server_name
    list_display = ('log_type','username','server_name','content',)
    readonly_fields = ('log_type','user','server','content')
    list_filter = ('log_type','user__alias','server__server_name',)


# class ServerForm(forms.ModelForm):
#     class Meta:
#         model = App
#
#     def __init__(self, *args, **kwargs):
#         forms.ModelForm.__init__(self, *args, **kwargs)
#         self.fields['application'].queryset = App.objects.all()

class ServerAdmin(admin.ModelAdmin):
    # forms = ServerForm
    readonly_fields = (
        'update_password_time',
        'cpu_model',
        # 'cpu_count',
        'physical_cpu_count',
        'cpu_core_count',
        'ram_size',
        'disk',
        'macaddress',
        'os_release',
        'manufacturer',
        'os_type',
        'os_distribution',
        'sn',
    )
    list_display = ('id','server_name','ipaddress','ssh_port','root_pwd','new_pwd',)
#    list_filter = ('operation','username','happened_time')
    search_fields = ('server_name','ipaddress')
    # raw_id_fields = ("application",)
    # filter_horizontal = ('application',)

# class ServerInline(admin.TabularInline):
#     model = Server
#     readonly_fields = ['id','server_name']
# class AppAdmin(admin.ModelAdmin):
#     inlines = [ServerInline,]

class ServerGroupAdmin(admin.ModelAdmin):
    filter_horizontal = ('servers',)

class TemplateAdmin(admin.ModelAdmin):
    filter_horizontal = (
        'services',
        'triggers',
    )
    # filter_horizontal = ('services','triggers',)

class ServiceAdmin(admin.ModelAdmin):
    filter_horizontal = ('items',)
    list_display = ('name','interval','plugin_name')
    #list_select_related = ('items',)


class TriggerExpressionInline(admin.TabularInline):
    model = TriggerExpression
    #exclude = ('memo',)
    #readonly_fields = ['create_date']
class TriggerAdmin(admin.ModelAdmin):
    list_display = ('name','severity','enabled')
    inlines = [TriggerExpressionInline,]
    #filter_horizontal = ('expressions',)
class TriggerExpressionAdmin(admin.ModelAdmin):
    list_display = ('id','trigger','service','service_index','specified_index_key','operator_type','data_calc_func','threshold','logic_type')

class ActionAdmin(admin.ModelAdmin):
     filter_horizontal = ('host_groups','hosts','user','user_group','operations')

# class MediaInline(admin.TabularInline):
#     model = Media
#
#
# class ActionOperationAdmin(admin.ModelAdmin):
#     inlines = [MediaInline,]


admin.site.register(Server,ServerAdmin)
admin.site.register(SoftwareList)
admin.site.register(CmdbEventLog,CmdbEventLogAdmin)
admin.site.register(App)
admin.site.register(EventLog,EventLogAdmin)
admin.site.register(ServerGroup,ServerGroupAdmin)
admin.site.register(OsUser)
admin.site.register(JumpServerAudit)
admin.site.register(Template)
admin.site.register(Service,ServiceAdmin)
admin.site.register(ServiceIndex)
admin.site.register(Trigger,TriggerAdmin)
admin.site.register(TriggerExpression,TriggerExpressionAdmin)
admin.site.register(Action,ActionAdmin)
admin.site.register(ActionOperation)
admin.site.register(Media)