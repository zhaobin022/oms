from cmdb import models
def cmdb_log(server , task_type , content):
    content_dic = {
        'task_type':task_type,
        'server':server,
        'content':content
    }
    cmdb_event = models.CmdbEventLog(**content_dic)
    cmdb_event.save()


def operation_log(log_type,user,server,content):
    obj = {}
    obj['log_type'] = log_type
    obj['user'] = user
    obj['server'] = server
    obj['content'] = content
    e = models.EventLog(**obj)
    e.save()