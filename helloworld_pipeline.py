import redis_connector as connector

client = connector.connect()
p = client.pipeline()
p.set("hello", "world")
p.incr("person")
p.execute()
hello_world_string = "Hello %s! You are person number %d I meet today." % (str(client.get("hello")), int(client.get("person")))
print(hello_world_string)