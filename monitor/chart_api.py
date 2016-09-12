import json


def get_ladata_series_key_list(redis_key , redis_obj,service_item):
    key_list_from_redis = redis_obj.lrange(redis_key,0,-1)
    ret_list = []

    for i in key_list_from_redis:
        i = json.loads(i)
        if i[0]:
            ret_list.append([i[1]*1000,float(i[0][service_item])]*100)
    return ret_list