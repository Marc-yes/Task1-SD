import redis
import time
import random

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insults_channel = "insults_channel"
pubsub_channel="pubsub_channel"

# Publish insults random
while True:
    print("\nEnviant insult random")
    insults=list(r.smembers(insults_channel))  # Retorna tots els insults de la llista
    
    if insults:
        random_insult = random.choice(insults)
        r.publish(pubsub_channel, random_insult)
        print(f"Insult enviat: {random_insult}")
    else:
        print("No hi ha insults disponibles.")

    
    time.sleep(5)           # Cada 5 segons