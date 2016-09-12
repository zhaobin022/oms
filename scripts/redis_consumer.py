import redis
pool = redis.ConnectionPool(host='localhost',db=1, port=6379)

redis_obj = redis.Redis(connection_pool=pool)
redis_con =redis_obj.pubsub()
redis_con.subscribe('test')
redis_con.parse_response()
print redis_con.parse_response()
