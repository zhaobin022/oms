__author__ = 'zhaobin022'
from optparse import OptionParser
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oms.settings")
import django
django.setup()
from saltapp.action_list import module_dic


if __name__ == '__main__':
    keys = ''
    for k in module_dic.keys():
        keys += k+"/"
    else:
        keys = keys.strip('/')

    usage = "usage: %%prog -s host1,host2 -g gorup1,group2 -f state_file (%s).action " % keys
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--server",
                  dest="host_list",
                  help="input host list -f web01,db01",
                  metavar='web01,db01'
                )
    parser.add_option("-g", "--group",
                  dest="group_list",
                  help="input group list -f group01,group02",
                  metavar='group01,group02'
                )
    parser.add_option("-f", "--statefile",
                  dest="state_file",
                  help="input group list -f state_file",
                  metavar='state_file'
                )
    (options, args) = parser.parse_args()
    if len(args) == 1 and  '.' in args[0]:
        module_name,action = args[0].split('.')
    else:
        parser.print_usage()
        parser.exit()

    if options.host_list and options.group_list and options.state_file:
        host_list = options.host_list.split(',')
        group_list = options.group_list.split(',')
        state_file = options.state_file
    else:
        parser.print_usage()
        parser.exit()


    if module_name in module_dic.keys():
        from saltapp.background.main import MainHandler
        main_handler = MainHandler(host_list,group_list,state_file,module_name,action)
        main_handler.handler()
    else:
        parser.print_usage()
        parser.exit()





