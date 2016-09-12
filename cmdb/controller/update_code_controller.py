#encoding: utf-8
from api.saltapi import SaltAPI
from conf.global_setttings import DANGER_COMMAND_LIST
from cmdb import models as cmdb_models
from utils.cmdb_utils import operation_log
import logging
logger = logging.getLogger('update_code')


class UpdateCodeHandler(object):
    def __init__(self,app_list, svn_version,request):
        self.app_list = app_list
        self.svn_version = svn_version
        self.req = request
        self.ret = {}

    def svn_update(self):

        app_list = cmdb_models.App.objects.filter(id__in=self.app_list)
        self.ret['status'] = True
        self.ret['result'] = []
        salt_api = SaltAPI()

        for a in app_list:
            if len(self.svn_version.strip()) == 0:
                command = '/usr/bin/svn update %s' % (a.app_path)
            else:
                command = '/usr/bin/svn update -r %s %s' % (self.svn_version,a.app_path)

            server_list = cmdb_models.Server.objects.filter(application=a)
            for s in server_list:
                result = salt_api.remote_execution(s.server_name, 'cmd.run',command)
                self.ret['result'].append(("%s   %s" %(s.application.app_name,s.server_name), s.ipaddress, result))
                operation_log(1,self.req.user,s,"command : %s , result : %s" % (command,result))
                logger.info(s.server_name+s.ipaddress)
                logger.info(result)


    def handler(self):
        self.svn_update()
        return self.ret
