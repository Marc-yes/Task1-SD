import pika

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Asegurarse de que la cola de textos exista
channel.queue_declare(queue='text_queue')

def send_text_to_service(text):
    """Enviar un texto al InsultService para que lo procese"""
    # Publicar el texto en la cola 'text_queue'
    channel.basic_publish(exchange='',
                          routing_key='text_queue',
                          body=text)
    print(f"[Cliente] Texto enviado a InsultService: {text}")

# Ejemplo de cliente que envía un texto
if __name__ == '__main__':
    # Cliente envía un texto con insultos
    text_to_send = "Eres un estúpido y un imbécil"
    send_text_to_service(text_to_send)

    # Aquí no necesitamos hacer nada más ya que el texto ya fue enviado al InsultService
    print("Cliente de prueba ejecutado. El texto fue enviado.")
