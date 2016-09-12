# -*- coding: UTF-8 -*-
from django.contrib import auth
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect
from user_center import models as user_center_models
import models
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import django.utils.timezone
from cmdb import models as cmdb_models
import logging
logger = logging.getLogger('online_request')

# Create your views here.
# @_auth('aa')


@login_required
def index(request):
    return render(request, 'index.html', {})

@login_required
def online_request_list(request):
    if request.method == 'GET':
        request_list = models.OnlineRequest.objects.all().order_by('-id')
        # for l in request_list:
        #     l.developer.select_related().all()
        return render(request, 'online_request/online_request_list.html', {'request_list': request_list})

@login_required
def get_reqest_list_json_api(request):
    if request.method == "POST":
        request_id = request.POST.get('id')
        try:
            request_item = models.OnlineRequest.objects.get(id=request_id)
        except Exception, e:
            request_item = None
        ret = {}

        if request_item:
            try:
                ret['status'] = True
                ret['msg'] = 'get result successfull !'

                # 初始化数据结构
                ret['data'] = {}

                ret['data']['online_request_status'] = request_item.online_request_status
            except Exception,e:
                logger.info( u'初始化数据结构'+str(e))

            try:
                # 填充申请时间

                ret['data']['request_time'] = (request_item.request_time + datetime.timedelta(hours=8)).strftime(
                    "%Y-%m-%d %H:%M:%S")
            except Exception,e:
                logger.info( u'填充申请时间'+str(e))

            try:
                # 填充开发人员
                ret['data']['developer'] = {}
                ret['data']['developer']['all'] = {}
                ret['data']['developer']['selected'] = {}
                if request_item.online_request_status == 1 and request.user.group.group_name == 'developer_group':
                    developers = request.user.team_member.all()
                else:

                    developer_group = user_center_models.UserGroup.objects.get(group_name='developer_group')
                    developers = developer_group.userprofile_set.select_related()

                for p in developers:
                    ret['data']['developer']['all'][p.id] = p.alias

                for p in request_item.developer.select_related():
                    ret['data']['developer']['selected'][p.id] = p.alias
            except Exception,e:
                logger.info( u'填充开发人员'+str(e))

            try:
                # 填充开发组长
                ret['data']['assign_developer_leader'] = {}
                userprofile =  request_item.assign_developer_leader
                ret['data']['assign_developer_leader'] = userprofile.id
            except Exception,e:
                logger.info(u'填充开发组长'+str(e))

            try:
                # 填充需求方
                ret['data']['require_side'] = {}
                ret['data']['require_side']['all_product_manager'] = {}
                ret['data']['require_side']['selected_product_manager'] = {}
                product_group = user_center_models.UserGroup.objects.get(group_name='product_manager')
                product_managers = product_group.userprofile_set.select_related()

                for p in product_managers:
                    ret['data']['require_side']['all_product_manager'][p.id] = p.alias

                for p in request_item.require_side.select_related():
                    ret['data']['require_side']['selected_product_manager'][p.id] = p.alias
            except Exception,e:
                logger.info( u'填充需求方'+str(e))

            try:
                # 功能类型
                ret['data']['function_type'] = {}
                ret['data']['function_type']['all'] = {}
                ret['data']['function_type']['selected'] = {}
                for k, v in request_item.function_type_choices:
                    if k == 3: break
                    ret['data']['function_type']['all'][k] = v
                if request_item.function_type:
                    ret['data']['function_type']['selected'] = request_item.function_type

            except Exception,e:
                logger.info( u'功能类型'+str(e))

            try:
                # 测试结果
                if request_item.test_result_tag:
                    ret['data']['test_result_tag'] = True
                else:
                    ret['data']['test_result_tag'] = False

            except Exception,e:
                logger.info( u'测试结果'+str(e))
            # 建议上线时间suggest_update_time
            try:
                if request_item.suggest_update_time:
                    ret['data']['suggest_update_time'] = (
                        request_item.suggest_update_time + datetime.timedelta(hours=8)).strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    ret['data']['suggest_update_time'] = False
            except Exception,e:
                logger.info( u'建议上线时间suggest_update_time'+str(e))

            try:
                # 版本标识
                if request_item.version_tag:
                    ret['data']['version_tag'] = request_item.version_tag
                else:
                    ret['data']['version_tag'] = False
            except Exception,e:
                logger.info( u'版本标识'+str(e))

            try:
                # 上线功能
                if request_item.online_function:
                    ret['data']['online_function'] = request_item.online_function
                else:
                    ret['data']['online_function'] = False
            except Exception,e:
                logger.info( u'上线功能'+str(e))

            try:
                # 上线项目
                ret['data']['app'] = {}
                ret['data']['app']['all'] = {}
                ret['data']['app']['selected'] = {}
                for p in models.App.objects.all():
                    ret['data']['app']['all'][p.id] = p.app_name

                for p in request_item.app.select_related().all():
                    ret['data']['app']['selected'][p.id] = p.app_name
            except Exception,e:
                logger.info( u'上线项目'+str(e))

            try:
                # 上线文件
                if request_item.online_files:
                    ret['data']['online_files'] = request_item.online_files
                else:
                    ret['data']['online_files'] = False

                try:
                    if request_item.developer_fun_confirm_before_online:
                        ret['data'][
                            'developer_fun_confirm_before_online'] = request_item.developer_fun_confirm_before_online.alias
                    else:
                        ret['data']['developer_fun_confirm_before_online'] = False
                except Exception, e:
                    logger.info( str(e))
            except Exception,e:
                logger.info( u'上线文件'+str(e))
                # ret['data']['developer_fun_confirm_before_online'] = {}
                # if request_item.developer_fun_confirm_before_online:
                #     p = request_item.developer_fun_confirm_before_online
                #     ret['data']['developer_fun_confirm_before_online'][p.id] = p.alias
            try:
                ret['data']['product_man_confirm_before_online'] = {}
                if request_item.product_man_confirm_before_online.select_related():
                    for p in request_item.product_man_confirm_before_online.select_related().all():
                        ret['data']['product_man_confirm_before_online'][p.id] = p.alias
            except Exception,e:
                logger.info( u'product_man_confirm_before_online'+str(e))

            try:
                ret['data']['test_confirm_before_online'] = {}
                ret['data']['test_confirm_before_online']['all'] = {}
                ret['data']['test_confirm_before_online']['selected'] = {}

                testing_group = user_center_models.UserGroup.objects.get(group_name='testing')

                testings = testing_group.userprofile_set.select_related()
                for p in testings:
                    ret['data']['test_confirm_before_online']['all'][p.id] = p.alias

                for p in request_item.test_confirm_before_online.select_related().all():
                    ret['data']['test_confirm_before_online']['selected'][p.id] = p.alias

            except Exception,e:
                logger.info(u'test_confirm_before_online'+str(e))
                # 上线前技术经理确认
            try:
                ret['data']['technical_man_fun_confirm_online'] = ''
                if request_item.technical_man_fun_confirm_online.all().count() != 0:
                    ret['data']['technical_man_fun_confirm_online'] = request_item.technical_man_fun_confirm_online.all()[
                        0].alias
                else:
                    ret['data']['technical_man_fun_confirm_online'] = False
            except Exception,e:
                logger.info(u'technical_man_fun_confirm_online'+str(e))

            try:
                ret['data']['white_box_test'] = {}
                if request_item.white_box_test.select_related():
                    for p in request_item.white_box_test.select_related().all():
                        ret['data']['white_box_test'][p.id] = p.alias
            except Exception,e:
                logger.info(u'white_box_test'+str(e))

            try:
                #运维上线确认
                ret['data']['maintenance_persion_comfirm'] = {}
                if request_item.maintenance_persion_comfirm.all().count() !=0:
                    ret['data']['maintenance_persion_comfirm'] = request_item.maintenance_persion_comfirm.all()[
                        0].alias
                else:
                    ret['data']['maintenance_persion_comfirm'] = False
            except Exception,e:
                logger.info( u'maintenance_persion_comfirm'+str(e))


            try:

                #运维经理上线确认
                ret['data']['maintenance_manager_comfirm'] = {}
                if request_item.maintenance_manager_comfirm.all().count() != 0:
                    ret['data']['maintenance_manager_comfirm'] = request_item.maintenance_manager_comfirm.all()[
                        0].alias
                else:
                    ret['data']['maintenance_manager_comfirm'] = False
            except Exception,e:
                logger.info(u'maintenance_manager_comfirm'+str(e))

            try:
                #测试上线后确认
                ret['data']['test_confirm_after_online'] = {}
                ret['data']['test_confirm_after_online']['all'] = {}
                ret['data']['test_confirm_after_online']['selected'] = {}
                for p in user_center_models.UserProfile.objects.filter(group__group_name='testing'):
                    ret['data']['test_confirm_after_online']['all'][p.id] = p.alias


                for p in request_item.test_confirm_after_online.select_related().all():
                    ret['data']['test_confirm_after_online']['selected'][p.id] = p.alias

            except Exception,e:
                logger.info(u'test_confirm_after_online'+str(e))




            try:
                #测试经理上线后确认

                ret['data']['test_man_confirm_after_online'] = {}
                if request_item.test_man_confirm_after_online.all().count() != 0:
                    ret['data']['test_man_confirm_after_online'] = request_item.test_man_confirm_after_online.all()[
                        0].alias
                else:
                    ret['data']['test_man_confirm_after_online'] = False

                # ret['data']['test_man_confirm_after_online'] = {}
                # ret['data']['test_man_confirm_after_online']['all'] = {}
                # ret['data']['test_man_confirm_after_online']['selected'] = {}
                # if request_item.test_man_confirm_after_online.select_related():
                #     ret['data']['test_man_confirm_after_online'] =  request_item.test_man_confirm_after_online.select_related().all()[0].username
            except Exception,e:
                logger.info(u'test_man_confirm_after_online'+str(e))


            try:

                #产品经理上线后确认
                ret['data']['product_man_confirm_after_online'] = {}
                if request_item.product_man_confirm_after_online.all().count() != 0:
                    ret['data']['product_man_confirm_after_online'] = request_item.product_man_confirm_after_online.select_related()[
                        0].alias
                else:
                    ret['data']['product_man_confirm_after_online'] = False
            except Exception,e:
                logger.info(u'product_man_confirm_after_online'+str(e))

            try:
                if request_item.cto_confirm:
                    ret['data']['cto_confirm'] = request_item.cto_confirm.alias
            except Exception,e:
                logger.info(u'cto_confirm'+str(e))




        else:
            ret['status'] = True
            ret['msg'] = 'get result successfull !'
            # 初始化数据结构
            ret['data'] = {}

            # 填充申请时间

            # ret['data']['request_time'] = (request_item.request_time+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S")

            # 填充开发人员
            ret['data']['developer'] = {}
            developer_group = user_center_models.UserGroup.objects.get(group_name='developer_group')
            developers = developer_group.userprofile_set.select_related()
            ret['data']['developer']['all_develper'] = {}
            for p in developers:
                ret['data']['developer']['all_develper'][p.id] = p.alias


            # 填充需求方
            ret['data']['require_side'] = {}
            product_managers = user_center_models.UserGroup.objects.get(group_name='product_manager').userprofile_set.all()

            ret['data']['require_side']['all_product_manager'] = {}
            for p in product_managers:
                ret['data']['require_side']['all_product_manager'][p.id] = p.alias

            try:
                # 填充开发组长
                ret['data']['assign_developer_leader'] = {}
                user_list = user_center_models.UserProfile.objects.filter(group__group_name='developer_group',admin_tag=True)
                for p in user_list:
                     ret['data']['assign_developer_leader'][p.id] = p.alias
            except Exception,e:
                logger.info(u'填充开发组长'+str(e))
                            #
            # #功能类型
            ret['data']['function_type'] = {}
            ret['data']['function_type']['all'] = {}
            for k, v in models.OnlineRequest.function_type_choices:
                if k == 3: break
                ret['data']['function_type']['all'][k] = v
            ret['data']['app'] = {}
            ret['data']['app']['all'] = {}
            for p in models.App.objects.all():
                ret['data']['app']['all'][p.id] = p.app_name

        return HttpResponse(json.dumps(ret))

    else:
        return HttpResponse("ok")

@login_required
def update_request_api(request):
    if request.method == 'POST':
        online_request_status = request.POST.get("online_request_status", None)

        if online_request_status == '0':
            online_function = request.POST.get('online_function', None)
            require_side = request.POST.getlist('require_side_create', None)
            function_type = request.POST.getlist('function_type', None)
            suggest_update_time = request.POST.get('suggest_update_time', None)
            assign_developer_leader_id = request.POST.get('assign_developer_leader', None)
            submit_dic = {}
            if function_type:
                if len(function_type) == 1:
                    function_type = int(function_type[0])
                elif len(function_type) == 2:
                    function_type = 3
                submit_dic['function_type'] = function_type

            if len(online_function) == 0 or len(require_side) == 0:
                return HttpResponseRedirect('codeonline/online_request_list/')

            if suggest_update_time:
                suggest_update_time = django.utils.timezone.datetime.strptime(suggest_update_time, "%Y-%m-%d %H:%M:%S")
                # suggest_update_time = datetime.datetime.strptime(suggest_update_time, "%Y-%m-%d %H:%M:%S")
                submit_dic['suggest_update_time'] = suggest_update_time

            if str(request.user.id) not in require_side:
                require_side.append(str(request.user.id))

            submit_dic['online_function'] = online_function
            assign_developer_leader = user_center_models.UserProfile.objects.get(id=assign_developer_leader_id)
            submit_dic['assign_developer_leader'] = assign_developer_leader

            submit_dic['online_request_status'] = 1
            logger.info(submit_dic)
            if function_type:
                submit_dic['function_type'] = function_type
            online_request = models.OnlineRequest.objects.create(**submit_dic)
            for id in require_side:
                u = models.UserProfile.objects.get(id=id)
                online_request.require_side.add(u)

        elif online_request_status == '1':
            request_item_id = request.POST.get('request_item_id', None)
            developers = request.POST.getlist('developer', None)
            version_tag = request.POST.get('version_tag', None)
            online_files = request.POST.get('online_files', None)
            app_ids = request.POST.getlist('app', None)
            online_request = models.OnlineRequest.objects.get(id=request_item_id)
            online_request.developer_fun_confirm_before_online = request.user
            request_item_dic = {}
            if version_tag:
                if len(version_tag) != 0:
                    online_request.version_tag = version_tag
            if online_files:
                if len(online_files) != 0:
                    online_request.online_files = online_files

            current_user_id = request.user.id
            if not current_user_id in developers:
                developers.append(current_user_id)
            developer_set = models.UserProfile.objects.filter(id__in=developers)
            for l in developer_set:
                online_request.developer.add(l)

            app_set = models.App.objects.filter(id__in=app_ids)
            for a in app_set:
                online_request.app.add(a)
            online_request.online_request_status = 2
            online_request.save()

        elif online_request_status == '2' and request.user.group.group_name == 'testing' and request.user.admin_tag:
            # {u'request_item_id': [u'5'], u'suggest_update_time': [u''], u'online_request_status': [u'2'], u'csrfmiddlewaretoken': [u'T8beRQLGLPPwQVTBKgZZaGB0JNWw6Rwv']}>
            request_item_id = request.POST.get('request_item_id', None)
            test_confirm_before_online = request.POST.getlist('test_confirm_before_online', None)
            request_item = models.OnlineRequest.objects.get(id=request_item_id)

            if str(request.user.id) not in test_confirm_before_online:
                test_confirm_before_online.append(str(request.user.id))
            if test_confirm_before_online:
                for p in test_confirm_before_online:
                    request_item.test_confirm_before_online.add(p)

            request_item.test_confirm_before_online.add(request.user)
            if request_item:
                request_item.online_request_status = 3
                request_item.save()
        elif online_request_status == '3' and request.user.group.group_name == 'technical_manager':
            request_item_id = request.POST.get('request_item_id', None)
            if request_item_id:
                request_item = models.OnlineRequest.objects.get(id=request_item_id)
                request_item.online_request_status = 4
                request_item.technical_man_fun_confirm_online.add(request.user)
                request_item.save()
        elif online_request_status == '4' and request.user.group.group_name == 'maintenance' and not request.user.admin_tag:
            request_item_id = request.POST.get('request_item_id', None)
            if request_item_id:
                request_item = models.OnlineRequest.objects.get(id=request_item_id)
                request_item.online_request_status = 5
                request_item.update_code_time = django.utils.timezone.now()
                request_item.maintenance_persion_comfirm.add(request.user)
                request_item.save()
        elif online_request_status == '5' and request.user.group.group_name == 'maintenance' and request.user.admin_tag:
            request_item_id = request.POST.get('request_item_id', None)
            if request_item_id:
                request_item = models.OnlineRequest.objects.get(id=request_item_id)
                request_item.online_request_status = 6
                request_item.maintenance_manager_comfirm.add(request.user)
                request_item.save()
        elif online_request_status == '6' and request.user.group.group_name == 'testing' and request.user.admin_tag:
            request_item_id = request.POST.get('request_item_id', None)
            test_confirm_after_online = request.POST.getlist("test_confirm_after_online",None)
            if request_item_id:
                if test_confirm_after_online:
                    if len(test_confirm_after_online) != 0:
                        request_item = models.OnlineRequest.objects.get(id=request_item_id)
                        request_item.online_request_status = 7
                        for i in test_confirm_after_online:
                            p = user_center_models.UserProfile.objects.get(id=i)
                            request_item.test_confirm_after_online.add(p)

                        request_item.test_man_confirm_after_online.add(request.user)
                        request_item.save()



                    else:
                        return HttpResponse.HttpResponseForbidden

                else:
                    return HttpResponse.HttpResponseForbidden
            else:
                return HttpResponse.HttpResponseForbidden
        elif online_request_status == '7' and request.user.group.group_name == 'product_manager':
            request_item_id = request.POST.get('request_item_id', None)
            if request_item_id:
                request_item = models.OnlineRequest.objects.get(id=request_item_id)
                request_item.online_request_status = 8
                request_item.product_man_confirm_after_online.add(request.user)
                request_item.save()


        return HttpResponseRedirect('codeonline/online_request_list/')
    else:
        return HttpResponse('create requeset fail')





@login_required
def dashboard(request):
    if request.method == 'GET':
        ret = {}
        ret['step_1'] = models.OnlineRequest.objects.filter(online_request_status=1).count()
        ret['step_2'] = models.OnlineRequest.objects.filter(online_request_status=2).count()
        ret['step_3'] = models.OnlineRequest.objects.filter(online_request_status=3).count()
        ret['step_4'] = models.OnlineRequest.objects.filter(online_request_status=4).count()
        ret['step_5'] = models.OnlineRequest.objects.filter(online_request_status=5).count()
        ret['step_6'] = models.OnlineRequest.objects.filter(online_request_status=6).count()
        ret['step_7'] = models.OnlineRequest.objects.filter(online_request_status=7).count()
        ret['step_8'] = models.OnlineRequest.objects.filter(online_request_status=8).count()
        ret['step_9'] = models.OnlineRequest.objects.filter(online_request_status=9).count()
        ret['server_count'] = cmdb_models.Server.objects.count()
        ret['app_count'] = cmdb_models.App.objects.count()
        return render(request, 'online_request/dashboard.html', {"ret":ret})

