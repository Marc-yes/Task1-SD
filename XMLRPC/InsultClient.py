from threading import Thread
import xmlrpc.client
import subprocess
import time
from xmlrpc.server import SimpleXMLRPCServer

#Funció per rebre els missatges del broadcast
def get_publication(insult):
    print("Insult obtingut", insult)

def proves():
    # El port que vols utilitzar per al servei
    port = 8008

    # Llançar el servidor `SubInsultService.py` amb el port desitjat
    subprocess.Popen(["python3", "SubInsultService.py", str(port)])

    # Esperar uns segons fins que el servidor s'iniciï
    time.sleep(2)

    # Crear el client per connectar-se a InsultService
    InsultService_proxy = xmlrpc.client.ServerProxy(f'http://localhost:{port}')

    # Provaem els mètodes del servidor
    # Afegeix una tasca
    print(InsultService_proxy.add_insult("perraco"))
    print(InsultService_proxy.add_insult("perraco"))
    print(InsultService_proxy.add_insult("cretino"))

    time.sleep(1)

    print(InsultService_proxy.get_insults())

    time.sleep(1)

    print(InsultService_proxy.subscribe("8010"))
    



def start_server():
    try:
        with SimpleXMLRPCServer(('localhost', 8010)) as server:
            server.register_introspection_functions()
            
            server.register_function(get_publication, 'get_publication')
            
            # Iniciar el "proves" en un thread separat
            thread2 = Thread(target=proves, daemon=True)
            thread2.start()

            print("Client en execució a http://localhost:8010...")
            server.serve_forever()
            
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == "__main__":
    start_server()


