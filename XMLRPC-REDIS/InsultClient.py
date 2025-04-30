import xmlrpc.client
import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0,
decode_responses=True)
channel_name = "Insult_Service"

# Crear client per connectar-se a InsultServer
s = xmlrpc.client.ServerProxy('http://localhost:6005')

insults=[]

# Afegir insults
print(s.add_insult("sorra"))
print(s.add_insult("tonto"))
print(s.add_insult("cretino"))

# Obtenir insults
print(s.get_insults())

# Subscripció al servei per rebre insults
channel=s.get_channel()
print(channel)

pubsub = client.pubsub()
pubsub.subscribe(channel_name)
print(f"Ets insultat per {channel_name}, waiting for insults...")

# Continuously listen for insults
for insult in pubsub.listen():
    if insult["type"] == "message":
        insults.append(insult['data'])
        print(f"Received: {insult['data']}")

