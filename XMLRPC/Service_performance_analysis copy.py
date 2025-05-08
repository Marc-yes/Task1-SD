import subprocess
import time
from multiprocessing import Process
import xmlrpc.client
import matplotlib.pyplot as plt

# Configuració
duration = 10  # segons a esperar abans de tancar el servei
target_port = 8005
client_url = f"http://localhost:{target_port}"

# Textos a inserir
num_insults = 1000
def generate_insults(n):
    return [f"insult_{i}" for i in range(n)]

# Llançar el servidor XMLRPC
def start_insult_service():
    subprocess.run(["python3", "InsultService.py"])

# Inserir insults a través del client
def push_insults():
    proxy = xmlrpc.client.ServerProxy(client_url)
    insults = generate_insults(num_insults)
    for insult in insults:
        proxy.add_insult(insult)

# Consultar insults a través del client
def query_insults():
    proxy = xmlrpc.client.ServerProxy(client_url)
    for _ in range(num_insults):
        proxy.get_insults()

# Test amb diversos clients en paral·lel
def run_test_with_clients(n_clients, task):
    print(f"\n--- Test amb {n_clients} client(s) per a {task.__name__} ---")

    # Llançar el servidor en un procés separat
    server_proc = Process(target=start_insult_service)
    server_proc.start()
    time.sleep(1.5)  # Esperar que el servidor estigui llest

    # Llançar clients paral·lels
    processes = []
    start = time.time()
    for _ in range(n_clients):
        p = Process(target=task)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    end = time.time()

    server_proc.terminate()
    server_proc.join()

    elapsed = end - start
    print(f"Temps total amb {n_clients} client(s): {elapsed:.2f} segons")
    return elapsed

if __name__ == "__main__":
    client_counts = [1, 2, 3]
    insert_times = []
    query_times = []

    for n in client_counts:
        insert_times.append(run_test_with_clients(n, push_insults))
        query_times.append(run_test_with_clients(n, query_insults))

    insert_speedups = [round(insert_times[0]/t, 2) for t in insert_times]
    query_speedups = [round(query_times[0]/t, 2) for t in query_times]

    print("\n--- Speedups inserció ---")
    for n, s in zip(client_counts, insert_speedups):
        print(f"{n} client(s): speedup = {s}")

    print("\n--- Speedups consulta ---")
    for n, s in zip(client_counts, query_speedups):
        print(f"{n} client(s): speedup = {s}")

    # Gràfics
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(client_counts, insert_times, marker='o', label='Inserció')
    plt.plot(client_counts, query_times, marker='o', label='Consulta')
    plt.title('Temps total per nombre de clients')
    plt.xlabel('Nombre de clients')
    plt.ylabel('Temps (s)')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(client_counts, insert_speedups, marker='o', label='Inserció')
    plt.plot(client_counts, query_speedups, marker='o', label='Consulta')
    plt.title('Speedup per nombre de clients')
    plt.xlabel('Nombre de clients')
    plt.ylabel('Speedup')
    plt.legend()

    plt.tight_layout()
    plt.show()
