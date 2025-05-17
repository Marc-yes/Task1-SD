import xmlrpc.client
import redis

# Definim els canals que s'utilitzaran
text_queue = "text_queue"

# Crear client per connectar-se a InsultServer
s = xmlrpc.client.ServerProxy('http://localhost:8006')

texts=["ets un subnormal", "semble un jugadorlol", "guapeton i sexy", "gilipollas simplement"] 

# Afegir texts
for text in texts:
    s.add_text(text)

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
for text in texts:
    print(r.blpop("text_queue", timeout=0))

