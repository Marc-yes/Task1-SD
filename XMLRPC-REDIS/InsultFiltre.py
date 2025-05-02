from threading import Thread
from xmlrpc.server import SimpleXMLRPCServer
import redis

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
channel_name="Insult_Service"
insults = "Insult_List"
queue_name = "Insult_queue"

results=[]


pubsub=None


# Lista de palabras a censurar
Local_list = ["subnormal", "jugadorlol", "gilipollas", "burro"]

def filter_text():
    while True:
        task = r.blpop(queue_name, timeout=0)  

        if task is not None:  # Evita errors si la coa está buida
            task_value = task[1]  # Extrau el missatge real
            task_censored = task_value  # Copia del missatge original

            # Reemplasa insults per "CENSORED"
            for insult in Local_list:
                task_censored = task_censored.replace(insult, "CENSORED")

            print(f"{task_censored}\n")


def recieve_publications():
    for insult in pubsub.listen():
        if insult["type"] == "message":
            Local_list.append(insult['data'])
      
            
def add_task(self, text):           ##FALTA ARREGLAR NENE##
    self.task_queue.put(text)
    self.id=self.id + 1
    
    return self.id

def get_results(self, index):       ##FALTA ARREGLAR NENE##
    return self.results[index]
           

def start_server():
    #Obtenim els insults
    Local_list = r.smembers(insults)
    
    #També ens subscibim per a anar afegint els nous insults
    pubsub = r.pubsub()
    pubsub.subscribe(channel_name)
    
    #Iniciar el servidor InsultService amb XMLRP 
    server = SimpleXMLRPCServer(("localhost", 6005), allow_none=True)
    server.register_function(add_insult, "add_insult")
    server.register_function(get_insults, "get_insults")
    server.register_function(get_channel, "get_channel")
    
    # Iniciar les diferents funcions en threads separats
    filter = Thread(target=filter_text, daemon=True)
    filter.start()
    
    reciever = Thread(target=recieve_publications, daemon=True)
    reciever.start()
    
    
# Inicia el servidor
if __name__ == "__main__":
    print("Iniciant Servidor InsultService en port=6379")
    start_server()