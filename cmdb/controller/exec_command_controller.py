#encoding: utf-8
from api.saltapi import SaltAPI
from conf.global_setttings import DANGER_COMMAND_LIST
from cmdb import models as cmdb_models
from utils.cmdb_utils import operation_log
import paramiko
import multiprocessing
import json
import logging
from conf.global_setttings import CMDB_THREAD_POOL_SIZE
logger = logging.getLogger('exec_command')



class ExecuteCommandHandler:
    def __init__(self,server_list, command,request,execute_type):
        logger.info('init')
        self.server_list = server_list
        self.command = command
        self.req = request
        self.execute_type = execute_type
        self.ret = {}


    def ssh_connect(self,h):
        logger.info('ssh_connect')
        s = paramiko.SSHClient()	#绑定实例
        s.load_system_host_keys()	#加载本机know host主机文件
        s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            s.connect(h.ipaddress,h.ssh_port,'root',h.root_pwd,timeout=5)   #连接远程主机
            stdin,stdout,stderr = s.exec_command(self.command)   #执行命令

            result = stdout.read(),stderr.read()    #读取命令结果

            self.ret['result'].append((h.server_name, h.ipaddress, result))
            operation_log(0,self.req.user,h,"ssh -- command : %s \n result : %s" %  (self.command,result))

            self.ret['status'] = True

            s.close()
        except Exception,e:
            self.ret['status'] = True
            result = str(e)
            self.ret['result'].append((h.server_name, h.ipaddress, result))
            operation_log(0,self.req.user,h,"ssh -- command : %s \n result : %s" %  (self.command,result))

    def deal_command(self):
        server_list = cmdb_models.Server.objects.filter(id__in=self.server_list)
        self.ret['result'] = []
        if self.execute_type == 'saltapi':
            self.ret['status'] = True

            salt_api = SaltAPI()
            for s in server_list:
                result = salt_api.remote_execution(s.server_name, 'cmd.run', self.command)
                self.ret['result'].append((s.server_name, s.ipaddress, result))
                operation_log(0,self.req.user,s,"saltapi -- command : %s \n result : %s" %  (self.command,result))
        elif self.execute_type == 'ssh':
            for h in server_list:
                self.ssh_connect(h)


    def filter_danger_command(self):
        for s in DANGER_COMMAND_LIST:
            flag = self.command.find(s)
            if flag != -1:
                self.ret['status'] = False
                self.ret['msg'] = u'危险的命令: %s' % self.command
                return True
        return False

    def handler(self):
        status = self.filter_danger_command()
        if status:
            return self.ret
        else:
            self.deal_command()

            return self.ret
