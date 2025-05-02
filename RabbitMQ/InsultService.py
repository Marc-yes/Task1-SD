import pika
import time

# Conexión al servidor RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declarar las colas donde se publicarán los insultos y los textos
channel.queue_declare(queue='insult_queue')
channel.queue_declare(queue='text_queue')  # Cola para los textos enviados por el cliente

class InsultService:
    def __init__(self, test_mode=False):
        self.insults = {"tonto", "idiota", "imbécil", "estúpido"}  # Lista de insultos predefinidos
        self.running = True
        self.test_mode = test_mode  # Nuevo parámetro para controlar el bucle
        print("InsultService started...")
        if self.test_mode:
            # Solo ejecutamos broadcast_insults una vez durante las pruebas
            self.broadcast_insults_once()
        else:
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
                insults_list = list(self.insults)
                message = ",".join(insults_list)
                channel.basic_publish(exchange='',
                                      routing_key='insult_queue',
                                      body=message)
                print(f"[InsultService] Sent insults: {message}")
            time.sleep(5)  # Esperar 5 segundos antes de enviar otro lote de insultos

    def broadcast_insults_once(self):
        """Enviar la lista de insultos solo una vez en el modo de prueba."""
        if self.insults:
            insults_list = list(self.insults)
            message = ",".join(insults_list)

            # En lugar de enviar al canal de RabbitMQ, lo agregamos al mock (si existe)
            channel.basic_publish(exchange='',
                                  routing_key='insult_queue',
                                  body=message)
            print(f"[InsultService] Sent insults once: {message}")

    def process_text(self, text):
        """Recibe el texto del cliente y lo pasa a la cola 'text_queue'"""
        channel.basic_publish(exchange='',
                              routing_key='text_queue',
                              body=text)
        print(f"[InsultService] Sent text to InsultFilter: {text}")

# Iniciar el servicio InsultService
if __name__ == '__main__':
    service = InsultService(test_mode=True)  # Activar modo de prueba

    # Simulamos que el cliente envía un texto después de un corto periodo
    time.sleep(2)  # Simulamos el tiempo en que el cliente envía el texto
    text_to_send = "Eres un tonto y un idiota"
    service.process_text(text_to_send)  # El cliente envía el texto al InsultService

    # Detener el servicio después de 20 segundos para evitar que se ejecute indefinidamente
    time.sleep(20)
    service.running = False
    print("InsultService stopped.")
