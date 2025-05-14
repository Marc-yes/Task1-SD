from threading import Thread
import redis

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
text_queue = "text_queue"

# Lista de palabras a censurar
insultList = ["tonto", "burro", "rata"]

print("InsultFiltre preparat per ser utilitzat...")

def censore_text():
    while True:
        task = r.blpop(text_queue, timeout=0)  

        if task:  # Evita errores si la cola está vacía
            text = task[1]  # Extrae el mensaje real (segundo elemento de la tupla)
            text_censored=text

            # Reemplazo de insultos por "CENSORED"
            for insult in insultList:
                text_censored = text_censored.replace(insult, "CENSORED")

            print(f"{text_censored}")
                

# Inicia el servidor
if __name__ == "__main__":
    censore_text()