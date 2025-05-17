import redis
import time

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "text_queue"

# Send multiple messages
messages = ["Fes la tasca burro", "Ens fiquem a treballar tonto?", "Has d'entregar la tasca 1 avui rata", "Ets molt majete", "burro, tonto, i a més rata"]
for message in messages:
    client.rpush(queue_name, message)
    print(f"Tasca: {message}")
    time.sleep(0.05) # Simulating a delay in task production