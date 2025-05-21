import Pyro4
import time
import concurrent.futures
import matplotlib.pyplot as plt
import sys


# Nombres fijos de los filtros
filter_names = [
    "PYRONAME:insultfilter_1",
    "PYRONAME:insultfilter_2",
    "PYRONAME:insultfilter_3",
]

def filter_text(filter_uri, text):
    proxy = Pyro4.Proxy(filter_uri)
    return proxy.filter_text(text)

def stress_test(num_nodes, num_requests):

    uris = filter_names[:num_nodes]
    texts = ["Este texto tiene un insulto idiota"] * num_requests
    
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = []
        for i, text in enumerate(texts):
            target_uri = uris[i % num_nodes]
            futures.append(executor.submit(filter_text, target_uri, text))

    end_time = time.time()
    total_time = end_time - start_time
    print(f"Tiempo total para {num_nodes} nodo(s): {total_time:.2f} segundos")
    return total_time

def main():
    if len(sys.argv) < 2:
        print("Debes introducir el numero de textos a censurar: stress_client.py <numero_textos>")
        sys.exit(1)

    try:
        textos = int(sys.argv[1])
    except ValueError:
        print("El argumento debe ser un número entero.")
        sys.exit(1)
    nodes = [1, 2, 3]
    times = []

    for n in nodes:
        print(f"\nProbando con {n} nodo(s)...")
        t = stress_test(n, textos)
        times.append(t)

    base_time = times[0]
    speedups = [base_time / t for t in times]

    # Gráficos
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


if __name__ == "__main__":
    main()
