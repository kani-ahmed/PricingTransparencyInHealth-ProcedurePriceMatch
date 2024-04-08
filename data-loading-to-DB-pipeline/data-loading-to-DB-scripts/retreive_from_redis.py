import redis
import json

# Connection details
redis_host = 'localhost'
redis_port = 6379
redis_db = 0

# Connect to Redis
r = redis.Redis(host=redis_host, port=redis_port, db=redis_db)

# Key where your JSON data is stored
key = 'summa_health_system_standardcharges'

# Fetch the JSON-encoded string from Redis
json_string = r.execute_command('JSON.GET', key, "$['File Summary'][0]['Hospital Name']")

# Decode the JSON string
decoded = json.loads(json_string)

# Assuming the result is a list, print the first element
print(decoded[0])
