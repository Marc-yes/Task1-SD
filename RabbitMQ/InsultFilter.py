import pika

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Asegurarse de que la cola existe
channel.queue_declare(queue='insult_queue')

class InsultFilter:
    def __init__(self):
        self.results = []

    def filter_text(self, text):
        # Censurar los insultos en el texto
        censored_text = text.replace("tonto", "CENSORED").replace("idiota", "CENSORED")
        print(f"[InsultFilter] Texto filtrado: {censored_text}")
        self.results.append(censored_text)
        return censored_text

    def callback(self, ch, method, properties, body):
        # Recibir el texto desde la cola
        text = body.decode()
        print(f"[InsultFilter] Texto recibido: {text}")
        # Filtrar el texto
        filtered_text = self.filter_text(text)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        # Configurar el consumidor para que llame al callback cuando llegue un mensaje
        channel.basic_consume(queue='insult_queue', on_message_callback=self.callback)
        print("[InsultFilter] Esperando textos... Para salir presiona CTRL+C")
        channel.start_consuming()

# Iniciar InsultFilter
if __name__ == '__main__':
    filter_service = InsultFilter()
    filter_service.start_consuming()
