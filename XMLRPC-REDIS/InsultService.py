import sys
from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
import time
import redis
import random

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

# Definim els canals que s'utilitzaran
insult_list = "insult_list"         #Definim la llista d'aquesta manera per a que es quedi a la base de dades de REDIS
pubsub_channel="pubsub_channel"

# Afegeix l'insult a la llista si no hi és
def add_insult(insult):
    r.sadd(insult_list, insult)

# Retorna tots els insults de la llista
def get_insults():
    return list(r.smembers(insult_list)) 


# Publish multiple insults
def insult_broadcast():
    while True:
        print("\nEnviant insult random")
        insults=get_insults()  # Retorna tots els insults de la llista
        
        if insults:
            random_insult = random.choice(insults)
            r.publish(pubsub_channel, random_insult)
            print(f"Insult enviat: {random_insult}")
        else:
            print("No hi ha insults disponibles.")

        
        time.sleep(5)           # Cada 5 segons
    

def start_server(port):
    try:
        print(f"Iniciant Servidor InsultService en port={port}")
        #Iniciar el servidor InsultService amb XMLRP 
        server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
        server.register_function(add_insult, "add_insult")
        server.register_function(get_insults, "get_insults")
        
        # Iniciar el "insult_broadcast" en un thread separat
        broadcast = Thread(target=insult_broadcast, daemon=True)
        broadcast.start()

        server.serve_forever()
    
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
    
# Inicia el servidor
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8006  # Assigna 8006 si no es passa cap argument
    start_server(port)
