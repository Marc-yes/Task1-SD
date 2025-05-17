import sys
from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import xmlrpc.client
import time

#Ens conectem al InsultService principal
master = xmlrpc.client.ServerProxy('http://localhost:8005')

def add_insult(insult):
    if master.sub_add_insults(insult) == 1:
        return "Insult afegit"
    
    return "L\'insult ja estava afegit"
    

#Funcio que retorna els insults
def get_insults():
    insults_recived = master.get_insults()
    return insults_recived


#Funcio que afegeix subscriptors a la taula
def subscribe(subscriber_port):
    if master.subscribe(subscriber_port):
        return "Subscriptor afegit"
    
    return "Subscriptor ja existent"



def start_server(port):
    try:
        with SimpleXMLRPCServer(('localhost', port)) as server:
            server.register_introspection_functions()
            
            server.register_function(add_insult, 'add_insult')
            server.register_function(get_insults, 'get_insults')
            server.register_function(subscribe, 'subscribe')

            print("InsultService en execució a http://localhost:", port)
            server.serve_forever()
            
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8006  # Assigna 8006 si no es passa cap argument
    start_server(port)
