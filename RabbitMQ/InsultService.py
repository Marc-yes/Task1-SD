import pika
import time

# Conexión al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar la cola donde se publicarán los textos
channel.queue_declare(queue='insult_queue')
channel.queue_declare(queue='text_queue')  # Nueva cola para los textos enviados por el cliente

class InsultService:
    def __init__(self):
        self.insults = {"tonto", "idiota", "imbécil", "estúpido"}  # Lista de insultos predefinidos
        self.running = True
        print("InsultService started...")
        self.broadcast_insults()

    def add_insult(self, insult):
        """Añadir un insulto a la lista si no está ya presente."""
        if insult not in self.insults:
            self.insults.add(insult)
            print(f"Insult added: {insult}")
            return True
        return False

    def get_insults(self):
        """Obtener todos los insultos almacenados."""
        return list(self.insults)

    def broadcast_insults(self):
        """Enviar la lista de insultos cada 5 segundos."""
        while self.running:
            if self.insults:
                # Convertir la lista de insultos en un solo mensaje
                insults_list = list(self.insults)
                message = ",".join(insults_list)  # Convertir la lista a un string separado por comas
                # Publicar el mensaje en la cola para que lo reciba el InsultFilter
                channel.basic_publish(exchange='',
                                      routing_key='insult_queue',
                                      body=message)
                print(f"[InsultService] Sent insults: {message}")
            time.sleep(5)  # Esperar 5 segundos antes de enviar otro lote de insultos

    def process_text(self, text):
        """Recibe el texto del cliente y lo pasa a la cola 'text_queue'"""
        channel.basic_publish(exchange='',
                              routing_key='text_queue',
                              body=text)
        print(f"[InsultService] Sent text to InsultFilter: {text}")

# Iniciar el servicio InsultService
if __name__ == '__main__':
    service = InsultService()