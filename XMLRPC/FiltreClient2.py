from threading import Thread
import time
import xmlrpc.client
# Crear client per connectar-se a InsultServer
s = xmlrpc.client.ServerProxy('http://localhost:8006')

texts = ["Hola tonto, que ets un tonto", "Vaya burro estas fet", "Vale crak"]

# Afegir insults
def fer_peticio(text):
    id=s.add_task(text)
    time.sleep(0.05)
    print(s.get_results(id))


threads = []
# Crear i iniciar treballadors
for text in texts:  # Crearem 3 treballadors
    worker = Thread(target=fer_peticio, args=(text,))
    worker.start()
    threads.append(worker)
    time.sleep(1)

for thread in threads:
    thread.join()

