import redis

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "task_queue"
channel_name = "insults"

print("InsultFiltre ready to be used...")

# Lista de palabras a censurar
insultlist = list(r.smembers(channel_name))  # Retorna tots els insults de la llista

while True:
    task = r.blpop(queue_name, timeout=0)  

    if task is not None:  # Evita errores si la cola está vacía
        task_value = task[1]  # Extrae el mensaje real (segundo elemento de la tupla)
        task_censored = task_value  # Copia del mensaje original

        # Reemplazo de insultos por "CENSORED"
        for insult in insultlist:
            task_censored = task_censored.replace(insult, "CENSORED")

        print(f"{task_censored}\n")