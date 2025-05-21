import pika

def receive_censored_text(ch, method, properties, body):
    """Recibir el texto censurado desde la cola censored_text_queue"""
    censored_text = body.decode()  # Decodificar el mensaje recibido
    print(f"[Client] Texto censurado recibido: {censored_text}")
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirmar que el mensaje fue procesado

def main():
    """Simula el cliente que envía textos al InsultService y recibe los textos censurados"""
    # Conexión al servidor RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # Asegurarse de que las colas existan
    channel.queue_declare(queue='insult_queue')
    channel.queue_declare(queue='text_queue')
    channel.queue_declare(queue='censored_text_queue')  # Cola para recibir los textos censurados

    # Escuchar la cola 'censored_text_queue' para recibir los textos censurados
    channel.basic_consume(queue='censored_text_queue', on_message_callback=receive_censored_text)

    # Enviar un texto al InsultService para ser censurado
    text_to_send = "Eres un tonto y un idiota"
    channel.basic_publish(exchange='',
                          routing_key='text_queue',
                          body=text_to_send)
    print(f"[Client] Texto enviado al InsultService: {text_to_send}")

    # Empezar a consumir mensajes de la cola
    print("[Client] Esperando al texto censurado...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
