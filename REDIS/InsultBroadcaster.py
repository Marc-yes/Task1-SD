import redis
import time

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0,
decode_responses=True)
channel_name = "insults"
pubsub_channel="events"

# Publish multiple insults
while True:
    insults=list(r.smembers(channel_name))  # Retorna tots els insults de la llista

    for insult in insults:
        r.publish(pubsub_channel, insult)
        print(f"{insult}")
    
    time.sleep(5)           # Cada 5 segons