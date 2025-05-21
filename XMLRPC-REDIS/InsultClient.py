import xmlrpc.client
import redis


# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Definim els canals que s'utilitzaran
pubsub_channel = "pubsub_channel"

# Crear client per connectar-se a InsultServer
s = xmlrpc.client.ServerProxy('http://localhost:8006')

insults=[]

# Afegir insults
s.add_insult("sorra")
s.add_insult("tonto")
s.add_insult("cretino")

# Obtenir insults
print(s.get_insults())


pubsub = r.pubsub()
pubsub.subscribe(pubsub_channel)
print(f"Ets insultat per {pubsub_channel}, waiting for insults...")

# Continuously listen for insults
for insult in pubsub.listen():
    if insult["type"] == "message":
        insults.append(insult['data'])
        print(f"Received: {insult['data']}")

