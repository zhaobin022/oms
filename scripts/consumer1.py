#!/usr/bin/env python
import pika
import pika_pool
import json
import time

params = pika.URLParameters(
   'amqp://guest:guest@localhost:5672/?'
   'socket_timeout=10&'
   'connection_attempts=2'
 )

pool = pika_pool.QueuedPool(
    create=lambda: pika.BlockingConnection(parameters=params),
    max_size=10,
    max_overflow=10,
    timeout=10,
    recycle=3600,
    stale=45,
)


def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep( body.count('.') )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)


with pool.acquire() as cxn:
    cxn.channel.queue_declare(queue='task_queue', durable=True)
    cxn.channel.basic_qos(prefetch_count=1)
    cxn.channel.basic_consume(callback,
                      queue='task_queue')
    cxn.channel.start_consuming()









'''


connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()
 
channel.queue_declare(queue='task_queue', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'
 
def callback(ch, method, properties, body):
    print " [x] Received %r" % (body,)
    time.sleep( body.count('.') )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)
 
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='task_queue')
 
channel.start_consuming()
 '''