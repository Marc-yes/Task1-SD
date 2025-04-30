from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
import time
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
channel_name = "Insult_Service"
insults_REDIS = "Insult_List"         #Definim la llista d'aquesta manera per a que es quedi a la base de dades de REDIS

local_list=[]

#Definim les funcions del servidor
# def add_insult(insult):
#     if not r.sismember(insults, insult):    # Comprovem si l'insult ja està a la llista
#         r.sadd(insults, insult)             # Afegeix l'insult a la llista si no hi és
#         return (f"Insult afegit: {insult}")
#     else:
#         return (f"L'insult {insult} ja existeix.")      #Si l'insult ja existeix, no l'afegim
def add_insult(insult):
    if insult not in local_list:
        local_list.append(insult)
        return "Insult afegit"
    return "L\'insult ja estava afegit"


def get_insults():
    return list(r.smembers(insults_REDIS))  # Retorna tots els insults de la llista

def get_channel():
    return channel_name

# Publish multiple insults
def insult_broadcast():
    while True:
        print ("Publicant Insults")
        for insult in local_list:
            r.sadd(insults_REDIS, insult)             # Afegeix l'insult a la llista. Si ja hi era, simplement no s'afegirà.
            ###################Hauria de posar un puto publishhh
        
        local_list.clear()
        
        time.sleep(5) # Simulating delay between insults
    

def start_server():
    try:
        #Iniciar el servidor InsultService amb XMLRP 
        server = SimpleXMLRPCServer(("localhost", 6005), allow_none=True)
        server.register_function(add_insult, "add_insult")
        server.register_function(get_insults, "get_insults")
        server.register_function(get_channel, "get_channel")
        
        # Iniciar el "insult_broadcast" en un thread separat
        broadcast = Thread(target=insult_broadcast, daemon=True)
        broadcast.start()

        server.serve_forever()
    
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
    
# Inicia el servidor
if __name__ == "__main__":
    print("Iniciant Servidor InsultService en port=6005")
    start_server()
