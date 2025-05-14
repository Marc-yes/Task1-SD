import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insults_channel = "insults_channel"

# Send multiple messages
insults = ["tonto", "burro", "rata", "tonto"]
for insult in insults:
    client.sadd(insults_channel, insult)             # Afegeix l'insult a la llista si no hi és

print (list(client.smembers(insults_channel)))  # Retorna tots els insults de la llista        