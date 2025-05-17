import redis
import sys

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insults_channel = "insults_channel"



# Recollir insult del paràmetre (si hi és)
if len(sys.argv) > 1:
    insult = sys.argv[1]
    client.sadd(insults_channel, insult)  # Afegeix insult si no hi és
    print(f"Insult afegit: {insult}")
else:
    print("No s'ha rebut cap insult per afegir.")


# print (list(client.smembers(insults_channel)))  # Retorna tots els insults de la llista        