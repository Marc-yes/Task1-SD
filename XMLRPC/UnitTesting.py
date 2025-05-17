from threading import Thread
import time
import xmlrpc.client
import unittest
from xmlrpc.server import SimpleXMLRPCServer
import xmlrpc.client

# # Crear client per connectar-se a InsultServer
insult_service = xmlrpc.client.ServerProxy('http://localhost:8005')
filtre_service = xmlrpc.client.ServerProxy('http://localhost:8006')
# server = SimpleXMLRPCServer(("localhost", 8002), allow_none=True)
insults=[]

def get_publication(actualization):
    global insults 
    insults = actualization
    print ("#################################################################################",actualization)

class TestInsultService(unittest.TestCase):

    def test_add_insult(self):
        self.assertEqual(insult_service.add_insult("sorra"), 'Insult afegit')
        self.assertEqual(insult_service.add_insult("ruc"), 'Insult afegit')

    def test_add_insult_repe(self):
        self.assertEqual(insult_service.add_insult("sorra"), 'L\'insult ja estava afegit')
        
    def test_add_insult_repetit(self):
        insults2 = ["sorra", "ruc"]
        self.assertEqual(insult_service.get_insults(), insults2)

    def test_subscribe(self):
        self.assertEqual(insult_service.subscribe(8002), "Subscriptor 8002 afegit!")
        
    def test_subscribe_repe(self):
        self.assertEqual(insult_service.subscribe(8002), "Subscriptor ja existent.")

    #Tot i q no es comprovi el broadcast directament, sí que es pot 
    #entendre que funcioni pel InsultFiltre, ja que aquest és subscriptor
    #del InsultService.py i esta poden filtra els texts gràcies a rebre
    #els insults per una publicació del servidor.
    
    # def test_get_publication(self):
    #     timeout = 15  # segons
    #     start = time.time()
        
    #     global insults
    #     publication = ["sorra", "ruc"]
    #     while not insults and (time.time() - start < timeout):
    #         time.sleep(0.2)            #Ens assegurem que ha passat el temps necessari
    #     self.assertEqual(insults, publication)
        
    def test_filter(self):
        time.sleep(6)
        id=filtre_service.add_task("Ets una sorra i un ruc")
        self.assertEqual(filtre_service.get_results(id), "Ets una CENSORED i un CENSORED")


# Crear el servidor tests per a poder rebre peticions
def start_testing():
    #s.subscribe(8002)
    
    # Crear el servidor XML-RPC
    server = SimpleXMLRPCServer(("localhost", 8002), allow_none=True)
    server.register_function(get_publication, 'get_publication')
    
    #Posem els tests en un thread per a poder provar les publicacions
    tests = Thread(target=unittest.main(), daemon=True)
    tests.start()

    print("Tests en execució a http://localhost:8002...")
    server.serve_forever()
    
    
# Inicia el servidor del filtre
if __name__ == "__main__":
    start_testing()
    