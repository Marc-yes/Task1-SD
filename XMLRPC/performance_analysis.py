import xmlrpc.client
import time
import threading

#XMLRPC
xmlrpc_filtre = xmlrpc.client.ServerProxy('http://localhost:8006')
xmlrpc_service = xmlrpc.client.ServerProxy('http://localhost:8005')

# Comprovarem quantes tasques es poden processar en un temps determinat
def perform_task(text):
    """Aquesta funció simula el client enviant una tasca de text al servidor per filtrar."""
    client_id=s.add_task(text)
    return s.get_results(client_id)  # Obtenim els resultats filtrats pel client 1

# Anàlisi de rendiment per a un únic node
def single_node_performance():
    start_time = time.time()
    texts = ["Ey, ets un tonto", "Ets molt guapet", "La sorra de ta mare"]
    
    for text in texts:
        perform_task(text)

    end_time = time.time()
    print(f"Temps total per procesar en un únic node: {end_time - start_time} segons.")

# Anàlisi d'escalabilitat estàtica (múltiples threads per una càrrega fixa)
def static_scaling_performance():
    start_time = time.time()
    threads = []
    texts = ["Ey, ets un tonto", "Ets molt guapet", "La sorra de ta mare"]

    # Creem múltiples threads per simular múltiples clients
    for text in texts:
        thread = threading.Thread(target=perform_task, args=(text,))
        threads.append(thread)
        thread.start()

    # Esperem que tots els threads acabin
    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Temps total amb escalabilitat estàtica: {end_time - start_time} segons.")

# Anàlisi d'escalabilitat dinàmica (ajustant el nombre de threads segons la càrrega)
def dynamic_scaling_performance():
    start_time = time.time()
    threads = []
    texts = ["Ey, ets un tonto", "Ets molt guapet", "La sorra de ta mare", "Un altre text a filtrar", "Filtrar més texts"]
    
    # Afegim tasques i ajustem els threads segons la cua
    for i, text in enumerate(texts):
        if len(threads) < 3:  # Limitem el nombre de threads actius a 3
            thread = threading.Thread(target=perform_task, args=(text,))
            threads.append(thread)
            thread.start()
        
        # Esperem que els threads acabin abans de crear-ne més
        if len(threads) == 3:
            for thread in threads:
                thread.join()
            threads = []  # Reiniciem els threads

    end_time = time.time()
    print(f"Temps total amb escalabilitat dinàmica: {end_time - start_time} segons.")

# Executeu les proves de rendiment
if __name__ == "__main__":
    print("Anàlisi de rendiment en un únic node:")
    single_node_performance()
    
    print("\nAnàlisi d'escalabilitat estàtica:")
    static_scaling_performance()
    
    print("\nAnàlisi d'escalabilitat dinàmica:")
    dynamic_scaling_performance()
