import redis
import time

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "task_queue"

# Send multiple messages
messages = ["burro burro i burro", "Somos la caña", "Vaya rata estas fet"]
for message in messages:
    client.rpush(queue_name, message)
    print(f"Tasca: {message}")
    time.sleep(3) # Simulating a delay in task production