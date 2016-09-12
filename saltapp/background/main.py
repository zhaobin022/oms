__author__ = 'zhaobin022'

from cmdb import models
from saltapp.action_list import module_dic
class MainHandler(object):
    def __init__(self,host_list,group_list,state_file,module_name,action):
        self.host_list = host_list
        self.group_list = group_list
        self.state_file = state_file
        self.module_name = module_name
        self.action = action
        self.fetch_all_host()

    def fetch_all_host(self):
        sever_list = []
        sever_list += models.Server.objects.filter(server_name__in=self.host_list)
        group_obj_list = models.ServerGroup.objects.filter(group_name__in=self.group_list)
        for g in group_obj_list:
            sever_list += g.servers.select_related()

        sever_list = set(sever_list)
        self.server_obj_list = list(sever_list)

    def handler(self):
        model_obj = module_dic[self.module_name](self.server_obj_list,self.action,self.state_file)
        if hasattr(model_obj,self.action):
            f = getattr(model_obj,self.action)
            f()
        else:
            print '''Don't have %s action !''' % self.action