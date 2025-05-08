from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import xmlrpc.client
import time

# RequestHandler personalitzat
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# # Servidor silenciat
# class QuietXMLRPCServer(SimpleXMLRPCServer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def log_request(self, code='-', size='-'):
#         pass  # No imprimeix res

# insults = ["hilipolles", "ruc"]
insults = []
subscribers = []

def add_insult(insult):
    if insult not in insults:
        insults.append(insult)
        return "Insult afegit"
    return "L'insult ja estava afegit"

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
            for subscriber in subscribers:
                try:
                    sub = xmlrpc.client.ServerProxy(f"http://localhost:{subscriber}")
                    sub.get_publication(insults)
                except Exception as e:
                    print(f"Error enviant insult a {subscriber}: {e}")
        time.sleep(5)

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

if __name__ == "__main__":
    start_server()
