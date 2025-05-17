import sys
from threading import Thread
import time
from xmlrpc.server import SimpleXMLRPCServer
import redis

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
text_queue = "text_queue"


# Lista de palabras a censurar
Local_list = ["subnormal", "jugadorlol", "gilipollas", "burro"]

def filter_text():
    while True:
        print(f"tasca:")
        task = r.blpop(text_queue, timeout=0)  
        if task is not None:  # Evita errors si la coa está buida
            task_value = task[1]  # Extrau el missatge real
            task_censored = task_value  # Copia del missatge original

            # Reemplasa insults per "CENSORED"
            for insult in Local_list:
                task_censored = task_censored.replace(insult, "CENSORED")

            print(f"{task_censored}\n")
            
        time.sleep(1)


            
def add_text(text):
    print(f"Text: {text}")
    r.rpush(text_queue, text)
    

           
def start_server(port):   
    #Iniciar el servidor InsultService amb XMLRP 
    server = SimpleXMLRPCServer(("localhost", port), allow_none=True)
    server.register_function(add_text, "add_text")
    
    # Iniciar les diferents funcions en threads separats
    filter = Thread(target=filter_text, daemon=True)
    filter.start()
    
    print(f"InsultFilter en execució a http://localhost:{port}...")
    server.serve_forever()
    
    
# Inicia el servidor
if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8006  # Assigna 8006 si no es passa cap argument
    start_server(port)