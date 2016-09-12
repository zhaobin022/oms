from AlertHandller.etc import settings
from oms import settings as oms_setttings
from cmdb import models
import time
import threading
import json
import subprocess
from AlertHandller.core.TriggerEventHandler import ActionHandler

class CheckServiceTimeoutHandler():
    def __init__(self):
        '''
         example :
                {
                46L: {u'LinuxCpu': {'last_update_time': 1466757690.175718}, u'LinuxMemory': {'last_update_time': 1466757690.175719}},
                47L: {u'LinuxCpu': {'last_update_time': 1466757814.251587}, u'LinuxMemory': {'last_update_time': 1466757801.226924}}
                }
        :return:
        '''
        self.all_config_dic = {}
        self.rabbit_con_pool = oms_setttings.RABBIT_POOL
        self.last_refresh_config_time = 0

    def get_template(self,server):
        templates = list(server.templates.select_related())
        templates_from_group = []
        for g in server.servergroup_set.all():
            templates_from_group.extend(g.templates.select_related())
        templates.extend(templates_from_group)

        return templates

    def get_services(self,server):
        templates = self.get_template(server)

        services = []
        for t in  set(templates):
            services.extend(t.services.select_related())

        services = set(services)
        service_dic = {}
        for s in services:
            service_dic[s.name] = {'last_update_time':time.time(),'interval':s.interval}
        # service_dic {u'LinuxCpu': {'last_update_time': ''}, u'LinuxMemory': {'last_update_time': ''}}
        return service_dic


    def refresh_config(self):
        server_list = models.Server.objects.all()
        for s in server_list:
            service_dic = self.get_services(s)
            if service_dic:
                if self.all_config_dic:
                    if self.all_config_dic.has_key(s.id):
                        # example service_dic : {u'LinuxCpu': {'last_update_time': ''}, u'LinuxMemory': {'last_update_time': ''}}
                        for k,v in service_dic.items():
                            if k not in self.all_config_dic[s.id].keys():
                                self.all_config_dic[s.id][k] = v
                            else:
                                if self.all_config_dic[s.id][k]['interval'] != v['interval']:
                                    self.all_config_dic[s.id][k]['interval']  = v['interval']
                    else:
                        self.all_config_dic[s.id] = service_dic
                else:
                    self.all_config_dic[s.id] = service_dic

        for server_id,services in self.all_config_dic.items():
            # v {u'LinuxCpu': {'last_update_time': ''}, u'LinuxMemory': {'last_update_time': ''}}
            try:
                server = models.Server.objects.get(id=server_id)
                templates = self.get_template(server)

                if len(templates) == 0:
                    del self.all_config_dic[server_id]
                    break


                current_services = self.get_services(server)
                for service_name,service_detail in services.items():
                    if service_name not in current_services.keys():
                        del self.all_config_dic[server.id][service_name]

            except models.Server.DoesNotExist:
                del self.all_config_dic[server_id]


    def judge_refresh_config(self):
        while True:
            if self.last_refresh_config_time == 0 or time.time() - self.last_refresh_config_time > settings.REFRESH_ALL_SERVER_CONFIG_INTERVAL:
                self.refresh_config()
                self.last_refresh_config_time = time.time()
            time.sleep(1)

    def update_service_latest_update_time(self,event):
        '''
        example : self.all_config_dic  {
                46L: {u'LinuxCpu': {'last_update_time': ''}, u'LinuxMemory': {'last_update_time': ''}},
                47L: {u'LinuxCpu': {'last_update_time': ''}, u'LinuxMemory': {'last_update_time': ''}}
            }
        '''
        server_id = int(event['server_id'])
        service_name = event['service_name']
        if self.all_config_dic.has_key(server_id):
            if self.all_config_dic[server_id].has_key(service_name):
                self.all_config_dic[server_id][service_name]['last_update_time'] = time.time()


    def update_service_status(self):
        def callback(ch, method, properties, event):
            event = json.loads(event)
            self.update_service_latest_update_time(event)
            ch.basic_ack(delivery_tag = method.delivery_tag)
        with self.rabbit_con_pool.acquire() as cxn:
            cxn.channel.queue_declare(queue=oms_setttings.RABBIT_CHECK_SERVICE_ALIVE_QUEUE, durable=True)
            cxn.channel.basic_qos(prefetch_count=1)
            cxn.channel.basic_consume(callback,
                              queue=oms_setttings.RABBIT_CHECK_SERVICE_ALIVE_QUEUE)
            cxn.channel.start_consuming()

    def check_service_timeout(self):
        for server_id , service_dic in self.all_config_dic.items():
            for service_name,service_detail in service_dic.items():
                if time.time() - service_detail['last_update_time'] > service_detail['interval']+2:
                    msg = '%d' % (time.time() - service_detail['last_update_time'] )

                    '''
                example : service_detail
                    u'LinuxCpu': {'last_update_time': '','alert_count',2}
                '''

                    host_obj = models.Server.objects.get(id=server_id)
                    host_groups = models.ServerGroup.objects.filter(servers=host_obj)
                    actions_from_hostgroup = models.Action.objects.filter(host_groups=host_groups)
                    actions_from_host = models.Action.objects.filter(hosts=host_obj)
                    actions = []
                    actions.extend(actions_from_hostgroup)
                    actions.extend(actions_from_host)
                    actions = list(set(actions))
                    for a in actions:
                        if service_detail.has_key('last_alert_time'):
                            if  time.time() - service_detail['last_alert_time'] > a.interval:
                                if service_detail.has_key('alert_count'):
                                    service_detail['alert_count'] += 1
                                else:
                                    service_detail['alert_count'] = 1
                                service_detail['last_alert_time'] = time.time()
                                tm_handler = TimeoutActionHandler(a,server_id,service_name,msg,service_detail['alert_count'])
                                tm_handler.handler()
                        else:
                            if service_detail.has_key('alert_count'):
                                service_detail['alert_count'] += 1
                            else:
                                service_detail['alert_count'] = 1
                            service_detail['last_alert_time'] = time.time()
                            tm_handler = TimeoutActionHandler(a,server_id,service_name,msg,service_detail['alert_count'])
                            tm_handler.handler()
                else:
                    if service_detail.has_key('alert_count'):
                        del service_detail['alert_count']

    def handler(self):
        refresh_config_thread= threading.Thread(target=self.judge_refresh_config)
        refresh_config_thread.start()

        check_service_timeout_thread = threading.Thread(target=self.update_service_status)
        check_service_timeout_thread.start()
        while True:
            check_service_timeout_thread= threading.Thread(target=self.check_service_timeout)
            check_service_timeout_thread.start()
            print self.all_config_dic
            time.sleep(1)



class TimeoutActionHandler(object):
    def __init__(self,action,server_id,service_name,msg,alert_count):
        self.action = action
        self.server_name = models.Server.objects.get(id=server_id).server_name
        self.service_name = service_name
        self.msg = msg
        self.alert_count = alert_count

    def email(self,m):
        print 'email'
        print 'Host : %s Service Name : %s Msg : Timeout %s second  ' % (self.server_name,self.service_name,self.msg)


    def sms(self,m):
        print 'sms'
        print 'Host : %s Service Name : %s Msg : Timeout %s second  ' % (self.server_name,self.service_name,self.msg)


    def script(self,m):
        print 'script'
        items = '"'
        for i in self.event_msg.items()[0][1]:
           items += i[0]+'|'
        items+='"'
        command = '%s %s %s %s %s ' % (m.script_path,self.host_obj.server_name,self.trigger.name,self.trigger.get_severity_display(),items)
        print command
        p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print p.stdout.read()


    def operation_handler(self,opt):
        for m in opt.medis_type.select_related():
            if hasattr(self,m.media_type):
                f = getattr(self,m.media_type)
                f(m)


    def handler(self):
        self.all_users = []
        user_list = self.action.user.select_related()
        user_list_from_group = []
        for g in self.action.user_group.select_related():
            user_list_from_group.extend( g.userprofile_set.all())

        self.all_users.extend(user_list_from_group)
        self.all_users.extend(user_list)
        for opt in self.action.operations.select_related():
            if opt.step <= self.alert_count:
                self.operation_handler(opt)
