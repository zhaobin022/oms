import redis
import time

pool = redis.ConnectionPool(host='localhost',db=1, port=6379)
redis_obj = redis.Redis(connection_pool=pool)
for i in range(100):
    redis_obj.publish('test',i)
    time.sleep(1)

