#coding:utf-8

import json
import time
import operator
import pika
from oms.settings import RABBIT_POOL


class DataHandler():
    def __init__(self,django_settings,redis_obj,host_obj,connect_redis=True):
        self.django_settings = django_settings
        self.host_obj = host_obj
        self.rabbit_con_pool = RABBIT_POOL
        if connect_redis:
            self.redis_obj = redis_obj


    def get_host_triggers(self):
        triggers = []
        templates = self.host_obj.templates.select_related()
        for t in templates:
            for trigger in t.triggers.select_related():
                if trigger.enabled:
                    triggers.append(trigger)
        return triggers

    def get_avg(self,data_set):
        return sum(data_set)/len(data_set)

    def get_max(self,data_set):
        return max(data_set)
    def get_last(self,data_set):
        return data_set[-1]

    def deal_expression(self,expression):
        redis_key = "StatusData_%d_%s_%s" %(self.host_obj.id,expression.service.name,'latest')

        time_range = expression.data_calc_args.split(',')[0]
        if len(expression.data_calc_args.split(',')) == 2:
            hit_arg =  int(expression.data_calc_args.split(',')[1])
        pick_point_number = int(time_range)*60+60/expression.service.interval
        time_range_data = self.redis_obj.lrange(redis_key,-pick_point_number,-1)
        correct_data = {}
        correct_data[expression.service_index.key] = []
        until_time = time.time() - int(time_range)*60
        for i in time_range_data:
            service_item , time_stamp = json.loads(i)
            if  until_time - time_stamp > 0:
                correct_data[expression.service_index.key].append(float(service_item[expression.service_index.key]))

        if hasattr(self,'get_%s'% expression.data_calc_func):

            fun = getattr(self,'get_%s'% expression.data_calc_func)
            ret = fun(correct_data[expression.service_index.key])
            if hasattr(operator,expression.operator_type):
                juge_fun = getattr(operator,expression.operator_type)
                return juge_fun(ret , expression.threshold)
        else:
            count = 0
            if hasattr(operator,expression.operator_type):
                juge_fun = getattr(operator,expression.operator_type)
            for i in correct_data[expression.service_index.key]:
                if juge_fun(i,expression.threshold):
                    count+=1
                    if count>=hit_arg:
                        return True
                else:
                    return False

    def load_service_data_and_calulating(self,trigger):
        express_ret_list = []
        notify_detail_ret = {}
        expression_ret_str = []
        notify_detail_ret[trigger.name] = []

        for expression in trigger.triggerexpression_set.order_by('id'):
            check_status = self.deal_expression(expression)
            if check_status:

                t_list = []
                t_list.append(expression.service_index.key)
                t_list.append(check_status)
                notify_detail_ret[trigger.name].append(t_list)
            expression_ret_str.append(str(check_status))
            if expression.logic_type:
                expression_ret_str.append(expression.logic_type)



        if eval(' '.join(expression_ret_str)):
            self.trigger_notifier(trigger,notify_detail_ret)
        else:
            trigger_event_key = "TriggerEvent_%d_%d*" %(self.host_obj.id,trigger.id)
            all_trigger_events = self.redis_obj.keys(trigger_event_key)
            for i in all_trigger_events:
                self.redis_obj.delete(i)


        print expression_ret_str
    def trigger_notifier(self,trigger,notify_detail_ret):
        print trigger
        print 'notify_detail_ret'
        print notify_detail_ret
        event = json.dumps([self.host_obj.id,trigger.id ,notify_detail_ret])

        with self.rabbit_con_pool.acquire() as cxn:
            cxn.channel.queue_declare(queue=self.django_settings.RABBIT_TRIGGER_NOTIFY_QUEUE, durable=True)
            cxn.channel.basic_publish(
                body=event,
                exchange='',
                routing_key=self.django_settings.RABBIT_TRIGGER_NOTIFY_QUEUE,
                properties=pika.BasicProperties(
                    content_type='application/json',
                    content_encoding='utf-8',
                    delivery_mode=2,
                )
            )

