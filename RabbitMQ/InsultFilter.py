import pika

# Conexión a RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Asegurarse de que las colas existan
channel.queue_declare(queue='insult_queue')
channel.queue_declare(queue='text_queue')  # Cola donde el texto será enviado

class InsultFilter:
    def __init__(self):
        self.insults_list = []  # Lista de insultos que recibimos
        self.results = []  # Resultados de textos filtrados

    def filter_text(self, text):
        """Censurar los insultos en el texto"""
        for insult in self.insults_list:
            text = text.replace(insult, "CENSORED")
        print(f"[InsultFilter] Texto filtrado: {text}")
        self.results.append(text)
        return text

    def callback_insults(self, ch, method, properties, body):
        """Recibir la lista de insultos desde la cola"""
        insults = body.decode()  # Decodificar el mensaje recibido
        self.insults_list = insults.split(",")  # Convertir el mensaje en una lista
        print(f"[InsultFilter] Recibidos los insultos: {self.insults_list}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_text(self, ch, method, properties, body):
        """Recibir el texto desde la cola y censurarlo"""
        text = body.decode()  # Decodificar el texto recibido
        print(f"[InsultFilter] Recibido texto para censurar: {text}")
        censored_text = self.filter_text(text)  # Censurar el texto
        ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirmar que el mensaje fue procesado

    def start_consuming(self):
        """Iniciar el consumo de los mensajes de las colas"""
        # Escuchar la cola de insultos
        channel.basic_consume(queue='insult_queue', on_message_callback=self.callback_insults)
        # Escuchar la cola de textos
        channel.basic_consume(queue='text_queue', on_message_callback=self.callback_text)
        print("[InsultFilter] Esperando insultos y textos... Para salir presiona CTRL+C")
        channel.start_consuming()

# Iniciar InsultFilter
if __name__ == '__main__':
    filter_service = InsultFilter()
    filter_service.start_consuming()
    