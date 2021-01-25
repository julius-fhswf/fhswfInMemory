import redis
#todo - change the host, port and db to your system settings
###redis connection parameters###
redis_host = "127.0.0.1"
redis_port = 6379
redis_db = 0
###end - redis connection parameters###
def connect():
    try:
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)
        return r
    except:
        e = "Error creating Redis connection"
        print(e)
        return None



    
