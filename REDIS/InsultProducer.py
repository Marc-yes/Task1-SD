import redis
import time

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0,
decode_responses=True)
channel_name = "insults"

# Send multiple messages
insults = ["tonto", "burro", "rata", "tonto"]
for insult in insults:
    
    client.sadd(insults, insult)             # Afegeix l'insult a la llista si no hi és
    print(f"Insult afegit: {insult}")

print (list(client.smembers(channel_name)))  # Retorna tots els insults de la llista        