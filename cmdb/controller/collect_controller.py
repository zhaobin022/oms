#encoding: utf-8
from api.saltapi import SaltAPI
from conf.global_setttings import SALT_API_ARGS
from sys import path
from conf.global_setttings import CMDB_THREAD_POOL_SIZE
from api.saltapi import SaltAPI
import threading
import logging
logger = logging.getLogger('web_apps')
from cmdb import models
from utils.cmdb_utils import cmdb_log
import json
import copy
from utils.threadpool import thread_pool

class UpdateAssetInfo(object):
    def __init__(self):
        try:
            self.sapi = SaltAPI()
            self.minion_list = self.sapi.all_online_minion()
            self.asset_info = []
            self.thread_pool_size = CMDB_THREAD_POOL_SIZE
        except Exception,e:
            logger.info("UpdateAssetInfo Init find online minion"+str(e))

    def update_all_asset_info(self):
        # logger.info(self.minion_list)
        minion_name_list_from_db = models.Server.objects.values_list('server_name', flat=True)
        minion_list_from_api = self.minion_list
        minion_need_insert = set(minion_list_from_api)-set(minion_name_list_from_db)
        minion_need_update = set(minion_name_list_from_db)-(set(minion_name_list_from_db)-set(minion_list_from_api))
        # minion_need_update = minion_name_list_from_db
        self.multitle_collect(list(minion_need_insert))
        if len(self.asset_info) > 0:
            for server_asset_info in self.asset_info:
                s = models.Server.objects.create(**server_asset_info)
                s.save()
                cmdb_log(s,0,json.dumps(server_asset_info))

        if len(minion_need_update) > 0:
            self.multitle_collect(list(minion_need_update))
            if len(self.asset_info) > 0:
                for server_asset_info in self.asset_info:
                    server = models.Server.objects.get(server_name=server_asset_info['server_name'])
                    update_dic = {}
                    log_dic = {}
                    if server:
                        for api_filed in server_asset_info.keys():
                            # if api_filed == 'ipaddress':continue
                            if hasattr(server,api_filed):
                                value = getattr(server,api_filed)
                                if value != server_asset_info[api_filed]:
                                    update_dic[api_filed] = server_asset_info[api_filed]
                                    log_dic[api_filed]={}
                                    log_dic[api_filed]['old_value'] = value
                                    log_dic[api_filed]['new_value'] = server_asset_info[api_filed]

                    if update_dic:
                        models.Server.objects.filter(id=server.id).update(**update_dic)
                        cmdb_log(server,1,json.dumps(log_dic))





    def __get_server_asset_info(self,tgt,tag):
        '''
        Salt API得到资产信息，进行格式化输出
        '''
        # ret = self.sapi.remote_noarg_execution(tgt,'grains.items')
        #     def remote_execution(self,tgt,fun,arg):
        try:
            ret = self.sapi.remote_execution(tgt,'grains.item','data')
            ret['data']['server_name'] = tgt
        except Exception,e:
            logger.info('collect server %s error ! May be not sync the grains . sync grains command is salt "*" saltutil.sync_grains .' % tgt)
        info = copy.deepcopy(ret['data'])
        self.asset_info.append(info)


    def multitle_collect(self,tgt):
        thread_pool(tgt,fun=self.__get_server_asset_info)
        '''
        #全局变量置空,避免多次请求的时候返回结果叠加
        self.asset_info=[]
        threads = []
        loop = 0
        numtgt = len(tgt)
        for i in range(0, numtgt, self.thread_pool_size):
            nkeys = range(loop*self.thread_pool_size, (loop+1)*self.thread_pool_size, 1)
            #实例化线程
            for i in nkeys:
                if i >= numtgt:
                    break
                else:
                    t = threading.Thread(target=self.__get_server_asset_info, args=(tgt[i],))
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
'''
    def handller(self):
        self.update_all_asset_info()

if __name__ == '__main__':
    asset_ino = UpdateAssetInfo()
    asset_ino.handller()