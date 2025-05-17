from threading import Thread
import xmlrpc.client
import subprocess
import time
import unittest
from xmlrpc.server import SimpleXMLRPCServer


# Llançar InsultService
#insult_service_process = subprocess.Popen(["python3", "InsultService.py"])

# Llançar SubInsultService
sub_insult_service_process = subprocess.Popen(["python3", "SubInsultService.py", "8006"])
time.sleep(2)
print(sub_insult_service_process.pid)
subInsultService_proxy = xmlrpc.client.ServerProxy('http://localhost:8006')


insults = 0

#Funció per rebre els missatges del broadcast
def get_publication(insult):
    global insults
    insults=insult


class TestInsultService(unittest.TestCase):    
    def test_add_insult(self):
        self.assertEqual(subInsultService_proxy.add_insult("sorra"), 'Insult afegit')

    def test_add_insult_repe(self):
        self.assertEqual(subInsultService_proxy.add_insult("sorra"), 'L\'insult ja estava afegit')
        time.sleep(2)
        
    def test_rebre_insults(self):
        insults2 = ["sorra"]
        self.assertEqual(subInsultService_proxy.get_insults(), insults2)

    def test_subscribe(self):
        self.assertEqual(subInsultService_proxy.subscribe(8010), "Subscriptor afegit")
        
    def test_subscribe_repe(self):
        self.assertEqual(subInsultService_proxy.subscribe(8010), "Subscriptor ja existent")

    # # def test_broadcast(self):
    # #     time.sleep(7)
    # #     global insults
    # #     self.assertEqual(insults, "sorra")
    
    def test_terminate_tests (self):
        #global insult_service_process
        global sub_insult_service_process
        print (sub_insult_service_process.pid)
        #insult_service_process.terminate()
        sub_insult_service_process.terminate()
        

def start_testing():
    try:
        with SimpleXMLRPCServer(('localhost', 8010)) as server:
            #time.sleep(2)
            #unittest.main()  # Aquesta línia executarà les proves automàticament
            
            server.register_introspection_functions()
            server.register_function(get_publication, 'get_publication')
            
            # Iniciar els tests en un thread separat
            #tests = Thread(target=unittest.main(), daemon=True)
            #tests.start()

            unittest.main() 
            
            print("Tests en execució a http://localhost:8010...")
            server.serve_forever()
            
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")

if __name__ == "__main__":
    start_testing()


