import redis
from oms import settings as django_settings
import json
from cmdb import models
import time
import subprocess
import sys


class DealTriggerEvents(object):
    def __init__(self,redis_obj):
        pool = redis.ConnectionPool(host=django_settings.REDIS_CONN['HOST'],db=django_settings.REDIS_CONN["DB"], port=django_settings.REDIS_CONN['PORT'])
        self.redis_obj = redis.Redis(connection_pool=pool)
        self.rabbit_con_pool = django_settings.RABBIT_POOL


    def juge_trigger(self,event):
        host_id,trigger_id,event_msg = event

        host_obj = models.Server.objects.get(id=host_id)
        trigger = models.Trigger.objects.get(id=trigger_id)
        host_groups = models.ServerGroup.objects.filter(servers=host_obj)
        actions_from_hostgroup = models.Action.objects.filter(host_groups=host_groups)
        actions_from_host = models.Action.objects.filter(hosts=host_obj)
        actions = []
        actions.extend(actions_from_hostgroup)
        actions.extend(actions_from_host)
        actions = list(set(actions))

        for a in actions:
            condition = a.conditions
            if condition == trigger.get_severity_display():
                trigger_event_key = "TriggerEvent_%d_%d_%d" %(host_obj.id,trigger.id,a.id)
                trigger_event_detail = self.redis_obj.get(trigger_event_key)
                if trigger_event_detail:
                    trigger_event_detail = json.loads(trigger_event_detail)
                    trigger_event_detail['alert_count'] +=1
                    last_alert_time = trigger_event_detail['last_alert_time']
                    if time.time() - last_alert_time > a.interval:
                        trigger_event_detail['last_alert_time'] = time.time()
                        self.redis_obj.set(trigger_event_key,json.dumps(trigger_event_detail))
                    else:
                        return
                else:
                    trigger_event_detail = {
                        'alert_count' : 1,
                        'last_alert_time' : time.time(),
                        'status' : 'fail'
                    }
                    self.redis_obj.set(trigger_event_key,json.dumps(trigger_event_detail))
                action_handler = ActionHandler(a,event_msg,host_obj,trigger,trigger_event_detail)
                action_handler.handler()


    def run(self):
        def callback(ch, method, properties, event):
            event = json.loads(event)
            self.juge_trigger(event)
            ch.basic_ack(delivery_tag = method.delivery_tag)
        with self.rabbit_con_pool.acquire() as cxn:
            cxn.channel.queue_declare(queue=django_settings.RABBIT_TRIGGER_NOTIFY_QUEUE, durable=True)
            cxn.channel.basic_qos(prefetch_count=1)
            cxn.channel.basic_consume(callback,
                              queue=django_settings.RABBIT_TRIGGER_NOTIFY_QUEUE)
            cxn.channel.start_consuming()




class ActionHandler(object):
    def __init__(self,action,event_msg,host_obj,trigger,trigger_event_detail):

        self.action = action
        self.event_msg = event_msg
        self.host_obj = host_obj
        self.trigger = trigger
        self.trigger_event_detail = trigger_event_detail
        trigger_name,items = self.event_msg.items()[0]
        self.msg = '''HOST : %s
TRIGGER : %s
LEVEL : %s''' % (self.host_obj.server_name,trigger_name,self.trigger.get_severity_display())
        for k,v in items:
            self.msg += '\nITEM : %s ' % k


    def email(self,m):
        print 'email'
        print self.msg
        print m.stmp_server


    def sms(self,m):
        print 'sms'

        print self.msg
        print m.gsm_moden


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
            if opt.step <= self.trigger_event_detail['alert_count']:
                self.operation_handler(opt)

