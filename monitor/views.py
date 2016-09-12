#coding:utf-8

from django.shortcuts import render
from django.shortcuts import render,HttpResponse
import json
from core import data_optimization
from core import data_processing
from monitor.chart_api import get_ladata_series_key_list
from monitor.controller.client_handler import ClientHandler
from django.views.decorators.csrf import csrf_exempt
from oms import settings
from cmdb import models
from utils import redis_conn
REDIS_OBJ = redis_conn.redis_conn(settings)

def client_configs(request,client_id):
    print("--->",client_id)
    config_obj = ClientHandler(client_id)
    config = config_obj.fetch_configs()

    if config:
        return HttpResponse(json.dumps(config))



def service_data_report(request):
    if request.method == 'POST':
        print("---->",request.POST)
        #REDIS_OBJ.set("test_alex",'hahaha')
        try:

            print('host=%s, service=%s' %(request.POST.get('client_id'),request.POST.get('service_name') ) )
            print
            data =  json.loads(request.POST['data'])
            #print(data)
            #StatusData_1_memory_latest
            client_id = request.POST.get('client_id')
            service_name = request.POST.get('service_name')
            data_saveing_obj = data_optimization.DataStore(client_id,service_name,data,REDIS_OBJ)

            #redis_key_format = "StatusData_%s_%s_latest" %(client_id,service_name)
            #data['report_time'] = time.time()
            #REDIS_OBJ.lpush(redis_key_format,json.dumps(data))

            #在这里同时触发监控
            host_obj = models.Server.objects.get(id=client_id)
            trigger_handler = data_processing.DataHandler(settings,REDIS_OBJ,host_obj)
            service_enable_triggers = trigger_handler.get_host_triggers()

            for trigger in service_enable_triggers:
                trigger_handler.load_service_data_and_calulating(trigger)
            print("service trigger::",service_enable_triggers)

        except IndexError as e:
            print('-->err:',e)


    return HttpResponse(json.dumps("---report success---"))


def display_chart(request):
    client_id = request.GET.get('client_id')
    server = models.Server.objects.get(id=client_id)
    templates = server.templates.select_related()
    templates_from_group = []
    for g in server.servergroup_set.all():
        templates_from_group.extend(g.templates.select_related())
    templates_from_group.extend(templates)

    services = []
    for t in  set(templates_from_group):
        services.extend(t.services.select_related())

    services = set(services)
    service_list = list(services)
    return render(request,'monitor/display_chart.html',{'server':server,'service_list':service_list})

@csrf_exempt
def get_latest(request):
    if request.method == 'GET':
        client_id = request.GET.get('client_id')
        service_name = request.GET.get('service_name')
        item_name = request.GET.get('item_name')
        data_type = request.GET.get('data_type')
        time_range = request.GET.get('time_range')
        if data_type == 'get_item_list':
            redis_key = "StatusData_%s_%s_%s" %(client_id,service_name,'latest')
            item_list = REDIS_OBJ.lrange(redis_key,-1,-1)

            return HttpResponse(json.dumps(json.loads(item_list[0])[0].keys()))
        elif data_type=='single_item_data':
            data_series_key_latest = "StatusData_%s_%s_%s" %(client_id,service_name,time_range)
            service_list = REDIS_OBJ.lrange(data_series_key_latest,0,-1)
            if time_range == 'latest':
                ret_list = []
                for i in service_list:
                    i = json.loads(i)
                    if i[0]:
                        ret_list.append([int(i[1]*1000),float(i[0][item_name])])
            else:
                ret_list = []
                for i in service_list:
                    i = json.loads(i)
                    if i[0]:
                        ret_list.append([int(i[1]*1000),float(i[0][item_name][0])])
            return HttpResponse(json.dumps(ret_list))
        elif data_type == 'get_latest_point':
            data_series_key_latest = "StatusData_%s_%s_%s" %(client_id,service_name,time_range)
            service_list = REDIS_OBJ.lrange(data_series_key_latest,-1,-1)
            if time_range == 'latest':
                ret_list = []
                for i in service_list:
                    i = json.loads(i)
                    if i[0]:
                        ret_list.append([int(i[1]*1000),float(i[0][item_name])])
            return HttpResponse(json.dumps(ret_list))


def monited_host(request):
    server_list = models.Server.objects.filter(templates=True)
    return render(request,'monitor/monited_host.html',{'server_list':server_list})


#def test(request):
#    add.delay(2, 2)
#    return HttpResponse('celery test')
