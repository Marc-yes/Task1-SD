import redis
import time
import subprocess
from multiprocessing import Process
import matplotlib.pyplot as plt

# Configuració
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
insults_channel = "insults_channel"
#n_pet = [1000, 3000, 5000]
n_pet = [10, 30, 50]
producer = "InsultProducer.py"

# Insults a enviar
def generate_insults(n):
    return [f"Insult_{i}" for i in range(n)]

# Llançar una instància de Producer
def start_producer():
    subprocess.run(["python3", producer])

# Benchmark per un nombre determinat de nodes
def run_test_with_nodes(n_nodes, act_n_pet):
    print(f"\n--- Test amb {n_nodes} node(s) de Service ---")

    # Netejar la cua abans de començar
    r.delete(insults_channel)

    # # Llançar els processos del filtre
    processes = []
    # for _ in range(n_nodes):
    #     p = Process(target=start_producer)
    #     p.start()
    #     processes.append(p)
    #     time.sleep(1)

    # time.sleep(2)
    insults = generate_insults(act_n_pet)
    
    # Enviar insults
    i=0
    
    start_time = time.time()        #comença el cronometro
    
    while (i<act_n_pet):
        j=0
        for j in range(n_nodes):
            if (i<act_n_pet):
                processes.append(subprocess.Popen(["python3", "InsultProducer.py", insults[i]]))
                i=i+1
            
        
        for proc in processes:          #Ens esperem a que acabin tots els nodes, per a no generar-ne més dels que volem.
            proc.wait()
        
        

    end_time = time.time()
    
    elapsed = end_time - start_time

    print(f"Temps total amb {n_nodes} node(s): {elapsed:.2f} segons")

    # # Finalitzar processos
    # for p in processes:
    #     p.terminate()
    #     p.join()
        
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
        
