import xmlrpc.client
import time
import threading
import matplotlib.pyplot as plt

# Crear client per connectar-se a InsultFilter
s = xmlrpc.client.ServerProxy('http://localhost:8006')

# Textos per cada prova
texts_100 = [
    "Ey, ets un tonto i una sorra.", 
    "Ets molt guapet, ho sabies?", 
    "La sorra de ta mare",
    "Un altre text a filtrar",
    "Filtrar més texts",
    "Un text més",
    "Un altre exemple",
    "Algú més que vulgui filtrar?",
    "Text random",
    "Últim text per provar"
]

texts_500 = texts_100 * 5  # 500 textos (replicant els de 100)
texts_1000 = texts_100 * 10  # 1000 textos (replicant els de 100)
texts_1500 = texts_100 * 15  # 1500 textos (replicant els de 100)
texts_2000 = texts_100 * 20  # 2000 textos (replicant els de 100)

# Crear un bloqueig per controlar l'accés concurrent a la connexió XML-RPC
lock = threading.Lock()

# Funció que simula l'enviament de tasques al servidor
def perform_task(text):
    with lock:  # Això garanteix que només un thread faci la petició al mateix temps
        task_id = s.add_task(text)  # Afegeix el text i rep l'ID (index)
        return task_id  # Retornem només l'ID per més tard recuperar el resultat

# 1. Anàlisi de rendiment per a un únic node
def single_node_performance(texts):
    start_time = time.time()  # Començar a mesurar el temps
    task_ids = []
    for text in texts:
        task_id = perform_task(text)
        task_ids.append(task_id)  # Guardem els IDs de les tasques

    # Esperar que totes les tasques hagin acabat abans de cridar get_results
    for task_id in task_ids:
        s.get_results(task_id)  # Obtenim els resultats filtrats utilitzant l'ID retornat

    end_time = time.time()  # Finalitzar mesura de temps
    return end_time - start_time

# 2. Anàlisi d'escalabilitat estàtica (múltiples threads per una càrrega fixa)
def static_scaling_performance(texts):
    start_time = time.time()
    threads = []
    task_ids = []
    
    # Creem múltiples threads per simular múltiples clients
    for text in texts:
        thread = threading.Thread(target=perform_task, args=(text,))
        threads.append(thread)
        thread.start()

    # Esperem que tots els threads acabin
    for thread in threads:
        thread.join()  # Espera que el thread acabi

    # Esperar que totes les tasques hagin acabat abans de cridar get_results
    for task_id in task_ids:
        s.get_results(task_id)  # Obtenim els resultats filtrats utilitzant l'ID retornat

    end_time = time.time()
    return end_time - start_time

# Funció per executar totes les proves de rendiment
def run_all_tests():
    results = {
        "single_node": [],
        "static_scaling": [],
    }
    
    # Afegir 100, 500, 1000, 1500 i 2000 textos per realitzar l'anàlisi
    for texts in [texts_100, texts_500, texts_1000, texts_1500, texts_2000]:
        print(f"\nExecutant anàlisis per a {len(texts)} textos...")
        
        print("Anàlisi de rendiment en un únic node:")
        results["single_node"].append(single_node_performance(texts))
        
        print("\nAnàlisi d'escalabilitat estàtica:")
        results["static_scaling"].append(static_scaling_performance(texts))

    return results

# Funció per calcular el Speedup
def calculate_speedup(T1, TN):
    return T1 / TN

# Generar gràfics dels resultats
def plot_results(results):
    x = ['100 Texts', '500 Texts', '1000 Texts', '1500 Texts', '2000 Texts']
    
    # Generar gràfiques per a cada tipus d'anàlisi
    plt.figure(figsize=(12, 8))
    
    plt.subplot(1, 2, 1)
    plt.bar(x, results['single_node'], color='blue')
    plt.xlabel('Nombre de Textos')
    plt.ylabel('Temps en segons')
    plt.title('Single Node')

    plt.subplot(1, 2, 2)
    plt.bar(x, results['static_scaling'], color='green')
    plt.xlabel('Nombre de Textos')
    plt.ylabel('Temps en segons')
    plt.title('Static Scaling')

    plt.tight_layout()
    plt.show()

# Funció per imprimir el Speedup per a cada anàlisi
def print_speedup(results):
    # Calcular Speedup per a cada volum de textos
    for i, num_texts in enumerate([100, 500, 1000, 1500, 2000]):
        T1 = results["single_node"][i]
        TN_static = results["static_scaling"][i]
        
        print(f"\nSpeedup per a {num_texts} textos:")
        print(f"Speedup (Static Scaling): {calculate_speedup(T1, TN_static)}")

if __name__ == "__main__":
    # Executar els anàlisis
    results = run_all_tests()

    # Imprimir el Speedup per a cada volum de textos
    print_speedup(results)

    # Generar gràfics
    plot_results(results)
