#encoding: utf-8
from django.shortcuts import render,HttpResponse
from api.saltapi import SaltAPI
import json
import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from cmdb.controller.collect_controller import UpdateAssetInfo
from cmdb.controller.exec_command_controller import ExecuteCommandHandler
from cmdb import models as cmdb_models
import forms
from cmdb.controller.deploy_soft_controller import DeploySoftware
from cmdb.controller.update_code_controller import UpdateCodeHandler
from cmdb.controller.update_server_pwd_controller import UpdateServerPassword
from utils.permission_ctl import permission_decorator
import logging
logger = logging.getLogger('web_apps')
import xlwt
import django.utils.timezone
import StringIO
from oms.settings import BASE_DIR
from django.core.servers.basehttp import FileWrapper
import os
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from jinja2 import Template
# Create your views here.

@login_required
@permission_decorator("maintenance")
def index(request):
    server_list = cmdb_models.Server.objects.all()
    return render(request,'cmdb/host_list.html',{'server_list':server_list})

@login_required
@permission_decorator("maintenance")
def cmdb_exe_command(request):

    if request.method == "GET":
        # minion_list = salt_api.all_online_minion()
        # server_list = models.ServerList.objects.filter(hostname__in=minion_list)
        server_list = models.Server.objects.all()
        # form = forms.ExecuteCommandForm()

        return render(request, 'cmdb/execute_command.html', {"server_list":server_list})

    elif request.method == "POST":
        form = forms.ExecuteCommandForm(request.POST)
        # logger.info( form.is_valid())
        ret = {}
        logger.info(request.POST)
        server_list = request.POST.getlist('server_list',None)
        if len(server_list) == 0:
            ret['status'] = False
            ret['msg'] = u'执行命令服务器列表不能为空'
            return HttpResponse(json.dumps(ret))
        command = request.POST.get('command',None)
        if len(command.strip()) == 0:
            ret['status'] = False
            ret['msg'] = u'命令不能为空'
            return HttpResponse(json.dumps(ret))
        execute_type = request.POST.get('execute_type').strip()
        if len(command.strip()) == 0:
            ret['status'] = False
            ret['msg'] = u'命令执行方式不能为空'
            return HttpResponse(json.dumps(ret))
        execute_command_handler = ExecuteCommandHandler(server_list,command,request,execute_type)
        ret = execute_command_handler.handler()
        # except Exception,e:
        #     logger.info(str(e))
        return HttpResponse(json.dumps(ret))


    server_list = cmdb_models.Server.objects.all()
    return render(request,'cmdb/execute_command.html',{})




@login_required
@permission_decorator("maintenance")
def update_server_info(request):
    update_controller = UpdateAssetInfo()
    update_controller.handller()
    ret = {"status":"finish"}
    return HttpResponse(json.dumps(ret))





@login_required
@permission_decorator("maintenance")
def deploy_software(request):
    if request.method == 'POST':
        ret = {}
        try:
            server_list = request.POST.getlist('server_list',None)
            if len(server_list) == 0:
                ret['status'] = False
                ret['msg'] = u'服务器列表不能为空'
                return HttpResponse(json.dumps(ret))
            software_list = request.POST.getlist('software_list',None)
            if len(software_list) == 0:
                ret['status'] = False
                ret['msg'] = u'软件列表不能为空'
                return HttpResponse(json.dumps(ret))
            server_list = models.Server.objects.filter(id__in=server_list).values_list('server_name', flat=True)
            software_list = models.SoftwareList.objects.filter(id__in=software_list).values_list('salt_state_module_name',
                                                                                                 flat=True)

            deploy = DeploySoftware(server_list=server_list, software_list=software_list,req=request)
            deploy_result_list = deploy.handler()
            ret['status'] = True
            ret['result'] = deploy_result_list
        except Exception,e:
            logger.info("deploy_software　view "+str(e))

        return HttpResponse(json.dumps(ret))
    elif request.method == "GET":
        server_list = models.Server.objects.all()
        software_list = models.SoftwareList.objects.all()
        # form = forms.DeploySoftwareForm()
        return render(request, 'cmdb/software_deploy.html', {'server_list':server_list,'software_list':software_list})

@login_required
@permission_decorator("maintenance")
def update_code(request):
    if request.method == "GET":
        app_list = models.App.objects.all()
        return render(request, 'cmdb/update_code.html', {"app_list":app_list})
    else:
        form = forms.UpdateCodeForm(request.POST)
        ret = {}
        app_list = request.POST.getlist('app_list',None)
        if len(app_list) == 0:
            ret['status'] = False
            ret['msg'] = u'应用列表不能为空'
        svn_version = request.POST.get('svn_version')
        update_code_handler = UpdateCodeHandler(app_list,svn_version,request)
        ret = update_code_handler.handler()
        return HttpResponse(json.dumps(ret))

@login_required
@permission_decorator("maintenance")
def update_server_password(request):
    if request.method=="GET":
        server_list = cmdb_models.Server.objects.all()
        return render(request,'cmdb/update_server_password.html',{'server_list':server_list})
    else:
        action_type = request.POST.get('action_type',None)
        server_list = request.POST.getlist('server_list[]',None)
        ret = {}
        action_type = action_type.strip()
        if len(action_type) == 0:
            ret['status'] = False
            return HttpResponse(json.dumps(ret))
        if action_type != 'gen_password' and action_type != 'ret_pass_tag'  :
            if len(server_list) == 0:
                ret['status'] = False
                return HttpResponse(json.dumps(ret))

        obj = UpdateServerPassword(action_type,server_list,request)
        ret = obj.handler()
        return HttpResponse(json.dumps(ret))



@login_required
@permission_decorator("maintenance")
def export_execel(request):
    if request.method == 'GET':
        response = HttpResponse(content_type='application/vnd.ms-excel')
        exportTime = django.utils.timezone.now()
        exportTimeStr  = exportTime.strftime("%Y%m%d")
        file_name = 'account_info_%s' % exportTimeStr
        response['Content-Disposition'] = 'attachment;filename=%s.xls' % file_name
        wb = xlwt.Workbook(encoding = 'utf-8')
        group_name_list = models.ServerGroup.objects.values('group_name')
        for r in group_name_list:
            sheet = wb.add_sheet(r['group_name'])
            #1st line
            sheet.write(0,0, 'Server Name')
            sheet.write(0,1, 'Ip Address')
            sheet.write(0,2, 'Port')
            sheet.write(0,3, 'Username')
            sheet.write(0,4, 'Password')
            sheet.write(0,5, 'New Password')

            row = 1
            for s in models.Server.objects.filter(servergroup__group_name=r['group_name']):
                sheet.write(row,0, s.server_name)
                sheet.write(row,1, s.ipaddress)
                sheet.write(row,2, s.ssh_port)
                sheet.write(row,3, 'root')
                sheet.write(row,4, s.root_pwd)
                sheet.write(row,5, s.new_pwd)

                row=row + 1

        else:
            sheet = wb.add_sheet('others')
            #1st line
            sheet.write(0,0, 'Server Name')
            sheet.write(0,1, 'Ip Address')
            sheet.write(0,2, 'Port')
            sheet.write(0,3, 'Username')
            sheet.write(0,4, 'Password')
            sheet.write(0,5, 'New Password')

            row = 1
            for s in models.Server.objects.filter(servergroup__group_name=None):
                sheet.write(row,0, s.server_name)
                sheet.write(row,1, s.ipaddress)
                sheet.write(row,2, s.ssh_port)
                sheet.write(row,3, 'root')
                sheet.write(row,4, s.root_pwd)
                sheet.write(row,5, s.new_pwd)


                row=row + 1

        output = StringIO.StringIO()
        wb.save(output)
        output.seek(0)
        response.write(output.getvalue())
        return response

def gen_jumpserver_mark(request):
    bookmark_list = []
    for s in models.Server.objects.all():
        bookmark = {
            "updated": 1458550920980,
            "name": s.server_name,
            "created": 1458550920980,
            "url": "ssh://root@%s:%d" % (s.ipaddress,s.ssh_port),
            "notes": "",
            "tags": ["Untagged"],
            "visits": 0,
            "updateSequenceNum": 1,
            "images": {"favicon": "data:image/x-icon;base64,AAABAAIABQkAAAEAIAAAAQAAJgAAABAQAAABAAgAaAUAACYBAAAoAAAABQAAABIAAAABACAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////SP///0j///9I////SP///w////8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A+AAAAPgAAAD4AAAA+AAAAPgAAAD4AAAA+AAAAPgAAAD4AAAAKAAAABAAAAAgAAAAAQAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACcnJwAoKSkAKikpACorKgArKysAKywrACwtLAAtLi0ALi4tAC0uLgAuLy4ALi8vAC8wLwAwMC8AMDAwADAxMAAxMjAAMTIxADIzMQAyMzIAMjMzADI0MgAyNDMAMzQ0ADQ0NAAzNTQANDU0ADQ2NAA0NjUANTY1ADU2NgA1NzUANjc2ADY3NwA3ODcANjg4ADc5NwA3OTgAODk4ADg5OQA4OjkAOTo5ADk6OgA5OzoAOjs6ADo7OwA6PDsAOzw7ADw9PAA8PjwAPD49ADw+PgA9Pz4APT8/AD1APgA/QD8AP0E/AEBBQQBAQkAAQEJBAEFCQQBBQ0IAQkRCAEJEQwBDRUMAREZFAEZIRwBGSUYAR0lHAEdKSABHSkkASEtJAElMSgBKTUsAS05MAE5QTwBnaGcAkXBUAG1wbgB+f34AgoOCAMOLWgDQlmMAj5CQAJCRkQChoqEAsrOyALO0swC3t7cAvL29AL29vQC+v74AxcXFAMbGxgDHx8cAyMjIAMrKygDLy8sAzMzMAM3NzQDOzs4Az8/PANHR0QDS0tIA1NTUANbW1gDb29sA39/fAOTk5ADo6OgA6enpAO3t7QDv7+8A8fHxAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABzc3Nzc3Nzc3Nzc3Nzc3Nzc1xoaGhoaGhoaGhoaGhac3NlNjEtJiEYEQ0IBQIAXXNzZDk0MC4kHxcRDAcEAV1zc2M9ODRPKSQdFBALBgNdc3NiQExVW1AoIhsVDwoGXnNzYUE/O1NXLighGRMOCV9zc2FDS1ZYNDAsJh0aEgxgc3NhRk5XNDQ0LyojHBYRYnNzYUhFVFlUODMvKCEcFGVzc2FKR0RUQDw3MiwnIBpmc3NhSklHQkE+OjUyKyUeZ3NzaGZpamtsbW9wbmxramhzc2hNcnJycnJycnJycmhNc3NRYWFhYXFRUVFRUVFRUXNzUVFRUVFRUVFRUVFRUlJz//8AAIABAACAAQAAgAEAAIABAACAAQAAgAEAAIABAACAAQAAgAEAAIABAACAAQAAgAEAAIABAACAAQAAgAEAAA=="}
              }
        bookmark_list.append(bookmark)
    filename = BASE_DIR+'/config_save/bookmarks.json'
    with open(filename, 'w') as f:
        f.write(json.dumps(bookmark_list))
    return HttpResponseRedirect(reverse('update_server_password'))

def gen_salt_config(request):
    salt_config_tpl = '''
{{ server_name }}:
  host: {{ ip }}   # The IP addr or DNS hostname
  user: root      # Remote executions will be executed as user fred
  passwd: {{ password }}  # The password to use for login, if omitted, keys are used
  port: {{ port }}
      '''

    template = Template(salt_config_tpl)
    config_text = ''
    for s in models.Server.objects.all():
        config_text += template.render(server_name=s.server_name,ip=s.ipaddress,password=s.root_pwd,port=s.ssh_port)
        config_text += '\n'
    filename = BASE_DIR+'/config_save/roster'

    with open(filename,'w') as f:
        f.write(config_text)
    return HttpResponseRedirect(reverse('update_server_password'))
