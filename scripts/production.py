#!/usr/bin/env python
import pika
import sys
import json
import time
import pika
import pika_pool
import threading

params = pika.URLParameters(
   'amqp://guest:guest@localhost:5672/?'
   'socket_timeout=10&'
   'connection_attempts=2'
 )

pool = pika_pool.QueuedPool(
    create=lambda: pika.BlockingConnection(parameters=params),
    max_size=20,
    max_overflow=10,
    timeout=10,
    recycle=3600,
    stale=45,
)


def fun(channel,i):
    channel.basic_publish(
        body=json.dumps({
             'type': 'banana',
             'description':i
        }),
        exchange='',
        routing_key='task_queue',
        properties=pika.BasicProperties(
            content_type='application/json',
            content_encoding='utf-8',
            delivery_mode=2,
        )
    )

def con_fun(i):
    with pool.acquire() as cxn:
        cxn.channel.queue_declare(queue='task_queue', durable=True)
        cxn.channel.basic_publish(
            body=json.dumps({
                 'type': 'banana',
                 'description':i,
            }),
            exchange='',
            routing_key='task_queue',
            properties=pika.BasicProperties(
                content_type='application/json',
                content_encoding='utf-8',
                delivery_mode=2,
            )
        )
        time.sleep(10)
threads = []
for i in range(10):
    t = threading.Thread(target=con_fun,args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()




'''
connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)

 
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='task_queue',
                      body=message,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
print " [x] Sent %r" % (message,)
connection.close()
'''
