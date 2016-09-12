#_*_coding:utf-8_*_

from api.saltapi import SaltAPI
import threading
from cmdb import models
from conf.global_setttings import CMDB_THREAD_POOL_SIZE
import logging
logger = logging.getLogger('web_apps')

from utils.cmdb_utils import operation_log


class DeploySoftware():
    def __init__(self,server_list,software_list,req):
        self.server_list = server_list
        self.software_list = software_list
        self.req = req
        self.result_list = []
        self.sapi = SaltAPI()
    def deploy_single_server(self,tgt):
        try:
            for i in self.software_list:
                temp = self.sapi.deploy(tgt,i)
                if len(temp['return'][0].keys()) == 0:
                    temp['return'][0]['status'] = False
                else:
                    temp['return'][0]['status'] = True
                temp['return'][0]['hostname'] = tgt
                try:
                    self.result_list.append(temp['return'][0])
                    operation_log(2,self.req.user,models.Server.objects.get(server_name=tgt),"software : %s,result %s" % (i,temp['return'][0]))
                except Exception,e:
                    logger.info('temp result formart error ' + str(e))

        except Exception,e:
            logger.info('deploy single sever loop'+str(e))

    def handler(self):
        threads = []
        loop = 0
        numtgt = len(self.server_list)
        for i in range(0, numtgt, CMDB_THREAD_POOL_SIZE):
            nkeys = range(loop*CMDB_THREAD_POOL_SIZE, (loop+1)*CMDB_THREAD_POOL_SIZE, 1)
            #实例化线程
            for i in nkeys:
                if i >= numtgt:
                    break
                else:
                    t = threading.Thread(target=self.deploy_single_server, args=(self.server_list[i],))
                    threads.append(t)
            #启动线程
            for i in nkeys:
                if i >= numtgt:
                    break
                else:
                    threads[i].start()
            #等待并发线程结束
            for i in nkeys:
                if i >= numtgt:
                    break
                else:
                    threads[i].join()
            loop = loop + 1

        return self.result_list
