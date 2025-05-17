import subprocess
import time
from multiprocessing import Process
import xmlrpc.client
import matplotlib.pyplot as plt
import redis

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


port=[8007, 8008, 8009, 8010, 8011, 8012, 8013, 8014, 8015, 8016]
n_pet=[1000, 3000, 5000, 10000, 13000, 18000, 20000]
insults=[]
max_nodes = 10  # Nombre màxim de nodes

# Configuració per al càlcul dinàmic
T = 0.1  # Temps de processament mitjà per missatge (segons per missatge)
C = 16  # Capacitat d'un sol treballador (missatges per segon)
total_time = 10


def init_insults(act_n_p):
    global insults
    i=0
    for i in range(act_n_p):
        insults.append(f"Insult_{i}")
    

def init_service(p):
    return subprocess.Popen(["python3", "InsultService.py", f"{p}"])

# Càlcul dinàmic del nombre de nodes basat en la fórmula
def calculate_required_nodes(act_n_pet):
    N = ((act_n_pet/total_time) * T) / C
    return N


def run_performance(n_nodes, act_n_p):
    global insults
    processes = []
    nodes = []
    
    for i in range(n_nodes):
        p=init_service(port[i])
        nodes.append(xmlrpc.client.ServerProxy(f'http://localhost:{port[i]}'))
        processes.append(p)

    #Assegurem que els servidors estan preparats per rebre peticions
    time.sleep(2)   
    
    start = time.time()
    
    #Repartim la carrega de treball per tants nodes com tinguem
    i=0
    while i < act_n_p:
        for j in range(n_nodes):
            if (i < act_n_p):               #Ens assegurem que queden insults per tractar
                nodes[j].add_insult(insults[i])
                i = i + 1            
    # print(f"\n{i} peticions enviades\n")
    
    end = time.time()
    
    elapsed = end - start
    
    for p in processes:
        p.terminate()
        
    processes.clear()
    
    print(f"Temps total amb {n_nodes} node(s): {elapsed:.2f} segons")

    r.spop('insult_list', r.scard('insult_list'))

    return elapsed
        
    
if __name__ == "__main__":
    
    times_single_node = []
    all_times = []   # Per guardar els temps de cada execució per cada nombre de nodes
    all_speedups = []  # Per guardar els speedups
    
    n_nodes_total=[]
    
    #Primer fem el cas amb un sol node per poder fer el speedup
    for actual_n_pet in n_pet:
    
        init_insults(actual_n_pet)
        
        elapsed = run_performance(1, actual_n_pet)
        
        times_single_node.append(elapsed)
    
    i=0
    
    for actual_n_pet in n_pet:
        print(f"\nProvant amb {actual_n_pet} peticions:")
        times = []
        
        nodes = calculate_required_nodes(actual_n_pet)

        nodes_be = int(nodes)
        
        if (nodes_be <=0):nodes_be = 1
        elif (nodes_be>max_nodes): nodes_be = 10

        n_nodes_total.append(nodes_be)
        

        elapsed = run_performance(nodes_be, actual_n_pet)
        times.append(elapsed)
        
        
        # Calcular speedups
        base_time = times_single_node[i]
        i=i+1

        speedup = (base_time / elapsed)
        # Guardar resultats per a la gràfica global
        all_speedups.append(speedup)
        all_times.append(times)
        
        
    for ti in times_single_node:
        print(f"{ti}")
        
        
    for ti in all_times:
        print(f"{ti}")
        
        
    for ti in n_nodes_total:
        print(f"{ti}")
        
        
    for ti in all_speedups:
        print(f"{ti}")
        
        
    # Mostrar resultats
    print("\n--- Speedups ---")
    for ts, t, n, s in zip(times_single_node, all_times, n_nodes_total, all_speedups):
        print (f"Temps single: {ts},  Temps en {n}: {t}")
        print(f"{n} node(s): speedup = {s}")
        
        
        
    # Generar gràfica amb tots els resultats
    plt.figure(figsize=(12, 6))

    # Gràfica temps total per nombre de nodes
    plt.subplot(1, 2, 1)
    for idx, actual_n_pet in enumerate(n_pet):
        plt.plot([n_nodes_total[idx]], all_times[idx], marker='o', label=f'{actual_n_pet} peticions')
    plt.title('Temps total per nombre de nodes')
    plt.xlabel('Nombre de nodes')
    plt.ylabel('Temps (segons)')
    plt.legend()

    # Gràfica speedup per nombre de nodes
    plt.subplot(1, 2, 2)
    for idx, actual_n_pet in enumerate(n_pet):
        plt.plot([n_nodes_total[idx]], all_speedups[idx], marker='o', label=f'{actual_n_pet} peticions')
    plt.title('Speedup per nombre de nodes')
    plt.xlabel('Nombre de nodes')
    plt.ylabel('Speedup')
    plt.legend()

    plt.tight_layout()
    plt.show()
    
    for n in n_nodes_total:
        print (f"s'han ussat {n} nodes")

    