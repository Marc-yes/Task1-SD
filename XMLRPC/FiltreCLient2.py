from threading import Thread
import time
import xmlrpc.client
# Crear client per connectar-se a InsultServer
s = xmlrpc.client.ServerProxy('http://localhost:8006')

texts = ["Hola tonto, que ets un tonto", "Vaya sorra estas feta", "Vale crak"]

# Afegir insults
def fer_peticio(text):
    id=s.add_task(text)
    time.sleep(1)
    print(s.get_results(id))


i=0
threads = []
# Crear i iniciar treballadors
for text in texts:  # Crearem 3 treballadors
    worker = Thread(target=fer_peticio, args=(text,))
    i=i+1
    worker.start()
    threads.append(worker)
    time.sleep(2)

for thread in threads:
    thread.join()

