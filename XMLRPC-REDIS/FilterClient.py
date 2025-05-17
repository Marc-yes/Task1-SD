import xmlrpc.client
import redis
import time

# Definim els canals que s'utilitzaran
text_set = "text_set"

# Crear client per connectar-se a InsultServer
s = xmlrpc.client.ServerProxy('http://localhost:8006')

texts=["ets un tonto", "semble un burro", "guapeton i sexy", "capsot simplement"] 

# Afegir texts
for text in texts:
    s.add_task(text)

time.sleep(2)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

print(list(r.smembers(text_set)))

