import redis
import time
import subprocess
from multiprocessing import Process
import matplotlib.pyplot as plt

# Configuració
client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
queue_name = "text_queue"
n_pet = [1000, 3000, 5000]
filter_script = "InsultFilter.py"

# Textos a enviar
def generate_texts(n):
    return [f"Missatge {i}: burro i rata, guapo, tonto" for i in range(n)]

# Llançar una instància de filtre
def start_filter():
    subprocess.run(["python3", filter_script])

# Benchmark per un nombre determinat de nodes
def run_test_with_nodes(n_nodes, act_n_pet):
    print(f"\n--- Test amb {n_nodes} node(s) de filtre ---")

    # Netejar la cua abans de començar
    client.delete(queue_name)

    # Llançar els processos del filtre
    processes = []
    for _ in range(n_nodes):
        p = Process(target=start_filter)
        p.start()
        processes.append(p)
        time.sleep(1)

    time.sleep(2)
    
    # Enviar textos
    texts = generate_texts(act_n_pet)
    
    start_time = time.time()
    for text in texts:
        client.rpush(queue_name, text)

    # Esperar que la cua es buidi
    while client.llen(queue_name) > 0:
        time.sleep(0.01)

    end_time = time.time()
    elapsed = end_time - start_time

    print(f"Temps total amb {n_nodes} node(s): {elapsed:.2f} segons")

    # Finalitzar processos
    for p in processes:
        p.terminate()
        p.join()
        
    processes.clear()

    return elapsed

if __name__ == "__main__":
    node_counts = [1, 2, 3]

    for actual_n_pet in n_pet:
        times = []
        print(f"Stress Tests amb {actual_n_pet} peticions\n")
        for n in node_counts:
            elapsed = run_test_with_nodes(n, actual_n_pet)
            times.append(elapsed)

        # Calcular speedups
        base_time = times[0]
        speedups = [round(base_time / t, 2) for t in times]

        # Mostrar resultats
        print("\n--- Speedups ---")
        for n, s in zip(node_counts, speedups):
            print(f"{n} node(s): speedup = {s}")

        # Gràfic
        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.plot(node_counts, times, marker='o')
        plt.title('Temps total per nombre de nodes')
        plt.xlabel('Nombre de nodes')
        plt.ylabel('Temps (segons)')

        plt.subplot(1, 2, 2)
        plt.plot(node_counts, speedups, marker='o', color='green')
        plt.title('Speedup per nombre de nodes')
        plt.xlabel('Nombre de nodes')
        plt.ylabel('Speedup')

        plt.tight_layout()
        plt.show()
        
