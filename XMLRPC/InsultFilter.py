from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
from threading import Thread
import xmlrpc.client
import queue

class InsultFilter:
    def __init__(self, insult_service_url):
        self.insult_service = xmlrpc.client.ServerProxy(insult_service_url)
        self.results = []
        self.task_queue = queue.Queue()
        self.id=-1

    #Si hi ha algun text a la coa, el processa
    def filter_text(self):
        while True:
            if not self.task_queue.empty():       
                text = self.task_queue.get()                    #Extraiem la tasca de la coa
                insults = self.insult_service.get_insults()
                filtered_text = text
                for insult in insults:
                    filtered_text = filtered_text.replace(insult, "CENSORED")
                
                self.results.append(filtered_text)
                
                print(f"Text filtrat: {filtered_text}")
                self.task_queue.task_done()                     # Marca la tasca com a completada
   
    def add_task(self, text):
        self.task_queue.put(text)
        self.id=self.id + 1
        
        return self.id

    def get_results(self, index):
        return self.results[index]

# Crear el servidor XML-RPC per al filtre
def start_filter_server():
    filter_service = InsultFilter("http://localhost:8005")      #Aqui indiquem on és l'insult service

    # Crear el servidor XML-RPC
    server = SimpleXMLRPCServer(("localhost", 8006), allow_none=True)
    server.register_instance(filter_service)
    
    # Crear i iniciar treballadors
    filtre = Thread(target=filter_service.filter_text, daemon=True)
    filtre.start()

    print("InsultFilter en execució a http://localhost:8005...")
    server.serve_forever()

# Inicia el servidor del filtre
if __name__ == "__main__":
    start_filter_server()