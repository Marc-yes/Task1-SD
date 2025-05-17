from threading import Thread
import xmlrpc.client
import subprocess
import time
from xmlrpc.server import SimpleXMLRPCServer


#Definim els texts que enviarem
texts = ["Ey, ets un tonto i un burro. No haguessa dit mai lo capsot que ets", "Ets molt guapet, ho sabies?", "tonto burro i a mes sexy"]


def proves():
    # El port que vols utilitzar per al servei
    port = 8005

    #Creem el proces que executa el InsultFilter
    p = subprocess.Popen(["python3", "InsultFilter.py", str(port)])
    
    # Esperar uns segons fins que el servidor s'iniciï
    time.sleep(2)

    # Crear client per connectar-se a InsultServer
    client_InsultFilter = xmlrpc.client.ServerProxy(f'http://localhost:{port}')

    for text in texts:
        id=client_InsultFilter.add_task(text)
        time.sleep(0.05)
        print(client_InsultFilter.get_results(id))
    
    
    time.sleep(2)
    
    p.terminate()
    
    
if __name__ == "__main__":
    proves()



