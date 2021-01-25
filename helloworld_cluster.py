from rediscluster import RedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "172.18.0.2", "port": "6379"}]
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

rc.set("Hello", "This is a clustered world!")

print(rc.get("Hello"))

print("Creating new users...")
start = int(rc.zcard("users"))
max_i = start + 60
print("Starting at user ", start)
for i in range(start, max_i):
    hash_address = i * 1024
    hash_key = "user:" + str(hash_address)
    hash_value = "Actually our " + str(i) + ". user"
    rc.hset("description", hash_key, hash_value)
    rc.zadd("users", {hash_key : i})

print("Users created: ", rc.zrange("users", start, -1))


