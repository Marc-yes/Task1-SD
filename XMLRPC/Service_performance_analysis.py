import subprocess
import time
from multiprocessing import Process
import xmlrpc.client
import matplotlib.pyplot as plt

n_pet=10000
insults=[]

#insult_service_url = "http://localhost:8005"
#s = xmlrpc.client.ServerProxy('http://localhost:8005')


def init_insults():
    global insults
    i=0
    for i in range(n_pet):
        insults.append(f"Insult_{i}")
        
    return insults
    

def init_service():
    subprocess.run(["python3", "InsultService.py"])


def run_performance(n_nodes):
    s = xmlrpc.client.ServerProxy('http://localhost:8009')
    global insults
    processes = []
    
    for i in range(n_nodes):
        p=Process(target=init_service)
        processes.append(p)
        p.start()

    time.sleep(2)   #Assegurem que els servidors estan preparats per rebre peticions
    
    start = time.time()
    
    for insult in insults:
        s.add_insult(insult)
    
    for _ in range(n_pet):
        s.get_insults()
    
    end = time.time()
    
    elapsed = end - start
    
    for p in processes:
        p.terminate()
        p.join()
        
    processes.clear()
    
    print(f"Temps total amb {n_nodes} node(s): {elapsed:.2f} segons")

    
    return elapsed
        
    
if __name__ == "__main__":
    nodes=[1, 2, 3]
    times = []
    
    for i in nodes:
        elapsed = run_performance(i)
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

    