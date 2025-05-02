from threading import Thread
import redis

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
text_queue = "task_queue"
insults_channel = "insults_channel"
pubsub_channel = "events"

# Lista de palabras a censurar
insultList = list(r.smembers(insults_channel))  # Retorna tots els insults de la llista
print (insultList)

print("InsultFiltre ready to be used...")

def censore_text():
    while True:
        task = r.blpop(text_queue, timeout=0)  

        if task:  # Evita errores si la cola está vacía
            text = task[1]  # Extrae el mensaje real (segundo elemento de la tupla)
            text_censored=text

            # Reemplazo de insultos por "CENSORED"
            for insult in insultList:
                text_censored = text_censored.replace(insult, "CENSORED")

            #print(f"{text_censored}")
            
            
def act_insultList(pubsub):
    # Continuously listen for insults
    for insult in pubsub.listen():
        if insult["type"] == "message":
            if insult["data"] not in insultList:
                insultList.append(insult['data'])
                #print(f"Received: {insult['data']}")
            

def start_server():
    # Subscribe to channel
    pubsub = r.pubsub()
    pubsub.subscribe(pubsub_channel)
    
    # Iniciar les diferents funcions en threads separats
    filter = Thread(target=act_insultList, args=(pubsub,), daemon=True)
    filter.start()
    
    censore_text()
    

# Inicia el servidor
if __name__ == "__main__":
    start_server()