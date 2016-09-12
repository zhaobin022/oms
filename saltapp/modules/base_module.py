import yaml
import os
import json
import sys
from saltapp.conf.settings import SALT_CONFIG_DIR,SALT_PLUGINS_DIR
from saltapp.background.task import TaskHandler
class BaseStateModule(object):
    def __init__(self,server_obj_list,action,state_file):
        self.server_obj_list = server_obj_list
        self.action = action
        self.state_file = state_file


    def jude_module_exists(self,module_name):
        module_path = os.path.join(SALT_PLUGINS_DIR,'%s.py' % module_name)
        sys.path.insert(0,SALT_PLUGINS_DIR)
        if os.path.isfile(module_path):
            current_module = __import__(module_name)
            return current_module
        else:
            print 'don\' have module %s' % module_name
    def apply(self):
        file_path = os.path.join(SALT_CONFIG_DIR,self.state_file)
        send_list = []
        if os.path.isfile(file_path):
            with open(file_path) as f:
                state_dic = yaml.load(f)
                for minion_id , module_dic in state_dic.items():
                    for module_part,sub_dic in module_dic.items():
                        module_name,action = module_part.split('.')
                        if self.jude_module_exists(module_name):
                            current_module = self.jude_module_exists(module_name)
                        if hasattr(current_module,module_name.capitalize()):
                            module_class = getattr(current_module,module_name.capitalize())
                            module_obj = module_class(self.server_obj_list,self.action,self.state_file)
                            ret = module_obj.syntax_parser(minion_id,module_name,sub_dic,action)
                            send_list.append(ret)
                        else:
                            print 'class %s  not exist!' % module_name.capitalize()

        else:
            print 'the yam file not exist %s ' %  file_path

        # print send_list
        task_handler = TaskHandler(self.server_obj_list ,send_list )
        task_handler.run()
    def parse_require(self,*args,**kwargs):
        sys.exit("must implement the function parse_require !!!!!" )

    def require(self,*args,**kwargs):
        self.require_list = []
        for require_module_dic in args[0]:
            require_module_name,require_module_value = require_module_dic.items()[0]
            current_module = self.jude_module_exists(require_module_name)
            if current_module:
                if hasattr(current_module,require_module_name.capitalize()):
                    state_class  =  getattr(current_module,require_module_name.capitalize())
                    state_obj = state_class(self.server_obj_list,self.action,self.state_file)
                    if hasattr(state_obj,"parse_require"):
                        parse_require = getattr(state_obj,"parse_require")
                        require = parse_require(require_module_value)
                        self.require_list.append(require)
                    else:
                        print 'don\'t have parse_require function'
            # print require_module_name,require_module_value
    def syntax_parser(self,minion_id,module_name,sub_dic,action):
        self.cmd = ''
        self.d={}
        for dic_detail in sub_dic:
            for k, v in dic_detail.items():
                if hasattr(self,k):
                    f = getattr(self,k)
                    f(v)
                else:
                    print ''' %s don't have key %s ''' % (self,k)
        else:
            if hasattr(self,action):
                f = getattr(self,action)
                self.d['cmd_list'] = []
                # self.d['cmd_list'].append(f(minion_id,sub_dic=sub_dic))
                f(minion_id,sub_dic=sub_dic,minion_id=minion_id)
                if hasattr(self,'require_list'):
                    self.d['require_list'] = self.require_list
                if hasattr(self,'file_dic'):
                    self.d['file_dic'] = self.file_dic
                    print 'in syntax_parser..............',self.file_dic
            else:
                print ''' Don't have %s function  ''' % (action)
        return self.d


