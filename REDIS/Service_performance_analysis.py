import redis
import time
from multiprocessing import Process
import matplotlib.pyplot as plt

# Configuració
redis_host = 'localhost'
redis_port = 6379
set_name = "insults_channel"
num_operations = 2000

# Funcions per a test

def insert_insults():
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    for i in range(num_operations):
        r.sadd(set_name, f"insult_{i}")

def query_insults():
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    for _ in range(num_operations):
        r.smembers(set_name)

def run_test_with_nodes(n_nodes, task):
    print(f"\n--- Test amb {n_nodes} node(s) per a {task.__name__} ---")

    client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    client.delete(set_name)

    # Preparar processos
    processes = []
    start_time = time.time()
    for _ in range(n_nodes):
        p = Process(target=task)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    end_time = time.time()

    elapsed = end_time - start_time
    print(f"Temps total amb {n_nodes} node(s): {elapsed:.2f} segons")
    return elapsed

if __name__ == "__main__":
    node_counts = [1, 2, 3]
    insert_times = []
    query_times = []

    for n in node_counts:
        insert_times.append(run_test_with_nodes(n, insert_insults))
        query_times.append(run_test_with_nodes(n, query_insults))

    # Calcular speedups
    insert_speedups = [round(insert_times[0] / t, 2) for t in insert_times]
    query_speedups = [round(query_times[0] / t, 2) for t in query_times]

    # Mostrar resultats
    print("\n--- Speedups d'inserció ---")
    for n, s in zip(node_counts, insert_speedups):
        print(f"{n} node(s): speedup = {s}")

    print("\n--- Speedups de consulta ---")
    for n, s in zip(node_counts, query_speedups):
        print(f"{n} node(s): speedup = {s}")

    # Gràfics
    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(node_counts, insert_times, marker='o', label='Inserció')
    plt.plot(node_counts, query_times, marker='o', label='Consulta')
    plt.title('Temps total per nombre de nodes')
    plt.xlabel('Nombre de nodes')
    plt.ylabel('Temps (s)')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(node_counts, insert_speedups, marker='o', label='Inserció')
    plt.plot(node_counts, query_speedups, marker='o', label='Consulta')
    plt.title('Speedups per nombre de nodes')
    plt.xlabel('Nombre de nodes')
    plt.ylabel('Speedup')
    plt.legend()

    plt.tight_layout()
    plt.show()
