import redis
#todo - change the host, port and db to your system settings
###redis connection parameters###
redis_host = "127.0.0.1"
redis_port = 55000
redis_db = 0
redis_password = "redispw" ###really bad idea
###end - redis connection parameters###
def connect():
    try:
        r = redis.Redis(host=redis_host, port=redis_port, db=redis_db, password=redis_password, charset="utf-8", decode_responses=True)
        return r
    except:
        e = "Error creating Redis connection"
        print(e)
        return None







    
