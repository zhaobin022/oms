#encoding: utf-8
__author__ = 'zhaobin022'
import threading
from conf.global_setttings import CMDB_THREAD_POOL_SIZE

def thread_pool( *args,**kwargs):
    #全局变量置空,避免多次请求的时候返回结果叠加
    threads = []
    loop = 0
    numtgt = len(args[0])
    for i in range(0, numtgt, CMDB_THREAD_POOL_SIZE):
        nkeys = range(loop*CMDB_THREAD_POOL_SIZE, (loop+1)*CMDB_THREAD_POOL_SIZE, 1)
        #实例化线程
        for i in nkeys:
            if i >= numtgt:
                break
            else:
                t = threading.Thread(target=kwargs['fun'], args=(args[0][i],args[1:]))
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