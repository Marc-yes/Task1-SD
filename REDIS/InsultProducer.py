import redis
import time

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0,
decode_responses=True)
channel_name = "insults_channel"

# Send multiple messages
insults = ["tonto", "burro", "rata", "tonto", "mariquita"]
for insult in insults:
    
    client.sadd(channel_name, insult)             # Afegeix l'insult a la llista si no hi és

print (list(client.smembers(channel_name)))  # Retorna tots els insults de la llista        