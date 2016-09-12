__author__ = 'zhaobin022'

from saltapp.conf.settings import RABBITMQ_INFO,RABBITMQ_STATE_SEND_QUEUE_PREFIX,STATE_TASK_RESULT_QUEUE_PREFIX
import pika
import json
from saltapp.models import StateTask
import time
import threading
class TaskHandler(object):
    def __init__(self,server_list,send_list):
        self.server_list = server_list
        self.send_list = send_list
        self.init_mq_channel()
        self.task_count = 0
        self.execute_count = 0
        self.task_dic = {}
    def close_connect(self):
        print 'in close_connect' , self.task_dic
        self.connection.close()
    def init_mq_channel(self):
        credentials = pika.PlainCredentials(RABBITMQ_INFO.get('username'), RABBITMQ_INFO.get('password'))
        parameters = pika.ConnectionParameters(RABBITMQ_INFO.get('ip'),RABBITMQ_INFO.get('port'),RABBITMQ_INFO.get('vhost'),credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.connection.add_timeout(190,self.close_connect)
        self.channel = self.connection.channel()
    def init_send_dic(self):
        t=StateTask()
        t.save()
        self.task_id = str(t.id)
        self.send_dic= {
            'callback_queue':STATE_TASK_RESULT_QUEUE_PREFIX % self.task_id,
            'data':self.send_list
        }
    def send_msg_to_mq(self):

        for host in self.server_list:
            self.task_count += 1
            queue_name = RABBITMQ_STATE_SEND_QUEUE_PREFIX % host.id
            self.task_dic[queue_name] = False
            print 'send to queue %s ' % queue_name
            print self.send_dic
            self.channel.queue_declare(queue=queue_name)
            self.channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(self.send_dic))
        self.begin_time = time.time()
    def wait_and_get_result(self):
        # self.channel.queue_declare(queue=STATE_TASK_RESULT_QUEUE_PREFIX % self.task_id)
        self.channel.queue_declare(queue=STATE_TASK_RESULT_QUEUE_PREFIX % self.task_id ,exclusive=True)

        def callback(ch, method, properties, body):
            self.execute_count += 1
            print " [x] Received %r" % (body,)
            data = json.loads(body)
            print  data[0].has_key('from'),'.......................'
            if data[0].has_key('from'):
                self.task_dic[data[0].get('from')] = True


        self.channel.basic_consume(callback, queue=STATE_TASK_RESULT_QUEUE_PREFIX % self.task_id, no_ack=True)

        print ' [*] Waiting for messages. To exit press CTRL+C'
        self.channel.start_consuming()
    def task_monitor(self):
        while True:
            spend_time = time.time() - self.begin_time
            if spend_time >= 5 or self.execute_count == self.task_count:
                try:
                    self.channel.close()
                    self.connection.close()
                except Exception:
                    self.connection.close()
                    break
                finally:
                    self.connection.close()
                    break
            print 'in loop'
            time.sleep(1)
        print 'exist loop'
    def run(self):
        self.init_send_dic()
        self.send_msg_to_mq()
        # t=threading.Thread(target=self.task_monitor,args=())
        # t.start()
        self.wait_and_get_result()
