import pika

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Asegurarse de que la cola existe
channel.queue_declare(queue='insult_queue')

def send_text_to_filter(text):
    # Enviar un texto a la cola
    channel.basic_publish(exchange='',
                          routing_key='insult_queue',
                          body=text)
    print(f"[Cliente] Texto enviado a InsultFilter: {text}")

# Ejemplo de cliente que envía un texto
if __name__ == '__main__':
    text_to_send = "Eres un tonto y un idiota"  # Ejemplo de texto con insultos
    send_text_to_filter(text_to_send)
