from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import xmlrpc.client
import time
import random

# RequestHandler personalitzat
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# # Servidor silenciat
# class QuietXMLRPCServer(SimpleXMLRPCServer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def log_request(self, code='-', size='-'):
#         pass  # No imprimeix res

insults = []
subscribers = []
tasks = []

# def add_insult(insult):
#     if insult not in insults:
#         insults.append(insult)
#         return "Insult afegit"
#     return "L'insult ja estava afegit"ç

def add_insult():
    while True:
        if tasks:
            insult = tasks.pop()
            insults.append(insult)
            print(f"Insult afegit: {insult}")  # Afegir log per veure què s'està afegint

        time.sleep(0.05)        #Afegim un poc de temps entre iteracions per a no saturar la cpu


#Rutina que utilitzaran els diferents nodes de subInsultService
def sub_add_insults(insult):
    if insult not in insults and insult not in tasks:
        tasks.append(insult)
        return 1
    
    return 0
    

#Funcio que retorna els insults
def get_insults():
    print(f"Insults enviats{insults}")
    return insults


#Funcio que afegeix subscriptors a la taula
def subscribe(subscriber_port):
    if subscriber_port not in subscribers:
        subscribers.append(subscriber_port)
        return 1
    return 0


#Funcio que envia un insult aleatori als subscriptors
def insult_broadcast():
    while True:
        if subscribers and insults:
            insult_rand=random.choice(insults)       #Triem un insult aleatori
            if insult_rand:
                for subscriber in subscribers:
                    try:
                        sub = xmlrpc.client.ServerProxy(f"http://localhost:{subscriber}")
                        print(f"Enviant insult {insult_rand} a {subscriber}...")
                        sub.get_publication(insult_rand)                                 #Els subs han de tenir aquest mètode per a poder obtenir els insults
                    
                    except Exception as e:
                        print(f"Error enviant insult a {subscriber}: {e}")
            else:
                print("No hi ha insults disponibles per enviar.")  # Missatge d'error si no hi ha insults
        
        time.sleep(5)


def start_server():
    try:
        with SimpleXMLRPCServer(('localhost', 8005), requestHandler=RequestHandler) as server:
            server.register_introspection_functions()
            
            server.register_function(sub_add_insults, 'sub_add_insults')
            server.register_function(get_insults, 'get_insults')
            server.register_function(subscribe, 'subscribe')

            # Iniciar el "insult_broadcast" en un thread separat
            thread = Thread(target=insult_broadcast, daemon=True)
            thread.start()
            
            # Iniciar el "add_insult" en un thread separat
            thread2 = Thread(target=add_insult, daemon=True)
            thread2.start()

            print("InsultService en execució a http://localhost:8005...")
            server.serve_forever()
            
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == "__main__":
    start_server()
