from xmlrpc.server import SimpleXMLRPCServer, XMLRPCDocGenerator
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import random
import time

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths=('/RPC2',)


insults = []
subscribers = []

#Definim les funcions del servidor
def add_insult(insult):
    if insult not in insults:
        insults.append(insult)
        return "Insult afegit"
    return "L\'insult ja estava afegit"

def get_insults():
    return insults

def subscribe(subscriber_url):
    if subscriber_url not in subscribers:
        subscribers.append(subscriber_url)
        return f"Subscriptor {subscriber_url} afegit!"
    return "Subscriptor ja existent."

def insult_broadcast():
    while True:
        if subscribers and insults:
            insult = random.choice(insults)
            for subscriber in subscribers:
                try:
                    #client = XMLRPCDocGenerator.client.ServerProxy(subscriber)
                    #client.receive_insult(insult)
                    print("Insult", insult)
                except Exception as e:
                    print(f"Error enviant insult a {subscriber}: {e}")
        time.sleep(5)

#Resgistrem les funcions amb un nom en concret
def start_server():
    try:
        with SimpleXMLRPCServer(('localhost', 8005), requestHandler=RequestHandler) as server:
            server.register_introspection_functions()
            
            server.register_function(add_insult, 'add_insult')
            server.register_function(get_insults, 'get_insults')
            server.register_function(subscribe, 'subscribe')

            # Iniciar el "insult_broadcast" en un thread separat
            thread = Thread(target=insult_broadcast, daemon=True)
            thread.start()

            print("InsultService en execució a http://localhost:8005...")
            server.serve_forever()
    
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")


# Inicia el servidor
if __name__ == "__main__":
    start_server()