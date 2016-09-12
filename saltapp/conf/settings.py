__author__ = 'zhaobin022'
import os

SALT_CONFIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'salt_configs')
SALT_PLUGINS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'modules')

RABBITMQ_INFO = {
    'ip':'localhost',
    'port':5672,
    'username':'test',
    'password':'test',
    'vhost':'/test'
}

RABBITMQ_STATE_SEND_QUEUE_PREFIX = 'STATE_TASK_QUEUE_%s'

STATE_TASK_RESULT_QUEUE_PREFIX = 'STATE_TASK_RESULT_QUEUE_%s'
