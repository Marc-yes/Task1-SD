import pika
import time
import random
import subprocess
from multiprocessing import Manager
import threading
import matplotlib.pyplot as plt
import sys

def launch_insult_service(node_id):
    return subprocess.Popen(['python3', 'InsultService.py', str(node_id)])

def launch_insult_filter(node_id):
    return subprocess.Popen(['python3', 'InsultFilter.py', str(node_id)])

def consume_censored_texts(stop_event, total_expected, received_list):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='censored_text_queue')

    def callback(ch, method, properties, body):
        censored_text = body.decode()
        received_list.append(censored_text)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        if len(received_list) >= total_expected:
            stop_event.set()

    channel.basic_consume(queue='censored_text_queue', on_message_callback=callback)

    print("Started consuming censored texts...")
    while not stop_event.is_set():
        connection.process_data_events(time_limit=1)

    channel.close()
    connection.close()
    print("Stopped consuming censored texts.")

def test_performance(node_count, total_texts):
    print(f"Starting performance test with {node_count} nodes...")

    insult_service_procs = [launch_insult_service(i+1) for i in range(node_count)]
    insult_filter_procs = [launch_insult_filter(i+1) for i in range(node_count)]

    time.sleep(5)

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='insult_queue')
    channel.queue_declare(queue='text_queue')
    channel.queue_declare(queue='censored_text_queue')

    insults = ["tonto", "idiota", "imbécil", "estúpido"]
    insult_message = ",".join(insults)
    channel.basic_publish(exchange='', routing_key='insult_queue', body=insult_message)

    texts_to_send = [f"Eres un {random.choice(insults)} y un {random.choice(insults)}" for _ in range(total_texts)]

    manager = Manager()
    received_texts = manager.list()
    stop_event = threading.Event()

    consumer_thread = threading.Thread(target=consume_censored_texts, args=(stop_event, total_texts, received_texts))
    consumer_thread.start()

    start_time = time.time()

    for text in texts_to_send:
        channel.basic_publish(exchange='', routing_key='text_queue', body=text)

    print(f"Sent {total_texts} texts to InsultService.")

    stop_event.wait(timeout=60)

    end_time = time.time()

    duration = end_time - start_time

    print(f"Test finished with {node_count} nodes.")
    print(f"Duration: {duration:.2f} seconds.")
    print(f"Received {len(received_texts)} censored texts.")

    for p in insult_service_procs + insult_filter_procs:
        p.terminate()
    consumer_thread.join()
    connection.close()

    return duration

def plot_results(node_counts, durations):
    baseline = durations[0]
    speedups = [baseline / d for d in durations]

    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(node_counts, durations, marker='o')
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

if __name__ == "__main__":
    node_counts = [1, 2, 3]

    if len(sys.argv) < 2:
        print("ERROR: Has de passar el número de textos a censurar com a paràmetre.")
        sys.exit(1)

    try:
        total_texts = int(sys.argv[1])
        if total_texts <= 0:
            raise ValueError()
    except ValueError:
        print("ERROR: El número de textos debe ser un entero positivo.")
        sys.exit(1)

    durations = []

    for nodes in node_counts:
        duration = test_performance(nodes, total_texts)
        durations.append(duration)

    plot_results(node_counts, durations)
