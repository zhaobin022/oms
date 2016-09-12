

import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)
os.environ['DJANGO_SETTINGS_MODULE'] ='oms.settings'
import django
import redis
django.setup()
from oms import settings as django_settings
from AlertHandller.core.TriggerEventHandler import DealTriggerEvents
from AlertHandller.core.CheckServiceTimeoutHandler import CheckServiceTimeoutHandler


def usage():
    print 'usage %s start' % sys.argv[0]



def check_service_timeout():
    check_service_timeout_handler = CheckServiceTimeoutHandler()
    check_service_timeout_handler.handler()



def start():
    pool = redis.ConnectionPool(host=django_settings.REDIS_CONN['HOST'],db=django_settings.REDIS_CONN["DB"], port=django_settings.REDIS_CONN['PORT'])
    redis_obj = redis.Redis(connection_pool=pool)
    newpid=os.fork()
    try:
        if newpid == 0:
            check_service_timeout()

        else:
            trigger_handler = DealTriggerEvents(redis_obj)
            trigger_handler.run()
    except KeyboardInterrupt:
        print 'Exit Kill my self  :)'
        os.kill(newpid,9)
if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        sys.exit(usage())
    else:
        arg = args[0].strip()
        current_module = sys.modules[__name__]
        if hasattr(current_module,arg):
            fun = getattr(current_module,arg)
            fun()
        else:
            usage()




