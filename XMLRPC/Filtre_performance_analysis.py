import subprocess
import time
from multiprocessing import Process
import xmlrpc.client
import matplotlib.pyplot as plt

port=[8007, 8008, 8009]
n_pet=[1000, 3000, 5000]
texts=[]


def init_insults(act_n_p):
    global texts
    i=0
    for i in range(act_n_p):
        texts.append(f"Ets un tonto, burro, i a mes un capsot")
    

def init_service(p):
    return subprocess.Popen(["python3", "InsultFilter.py", f"{p}"])


def run_performance(n_nodes, act_n_p):
    global texts
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
            if (i < act_n_p):               #Ens assegurem que queden texts per tractar
                nodes[j].add_task(texts[i])
                i = i + 1
    
    end = time.time()
    
    elapsed = end - start
    
    for p in processes:
        p.terminate()
        
    processes.clear()
    
    print(f"Temps total amb {n_nodes} node(s): {elapsed:.2f} segons")

    return elapsed
        
    
if __name__ == "__main__":
    nodes=[1, 2, 3]
    
    for actual_n_pet in n_pet:
        print(f"\nProvant amb {actual_n_pet} peticions:")
        times = []
    
        init_insults(actual_n_pet)
        
        for i in nodes:
            elapsed = run_performance(i, actual_n_pet)
            times.append(elapsed)
        
        # Calcular speedups
        base_time = times[0]
        speedups = [round(base_time / t, 2) for t in times]
        
        # Mostrar resultats
        print("\n--- Speedups ---")
        for n, s in zip(nodes, speedups):
            print(f"{n} node(s): speedup = {s}")

        # Gràfic
        plt.figure(figsize=(10, 5))

        plt.subplot(1, 2, 1)
        plt.plot(nodes, times, marker='o')
        plt.title('Temps total per nombre de nodes')
        plt.xlabel('Nombre de nodes')
        plt.ylabel('Temps (segons)')

        plt.subplot(1, 2, 2)
        plt.plot(nodes, speedups, marker='o', color='green')
        plt.title('Speedup per nombre de nodes')
        plt.xlabel('Nombre de nodes')
        plt.ylabel('Speedup')

        plt.tight_layout()
        plt.show()

    