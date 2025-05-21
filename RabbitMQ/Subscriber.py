import pika
import sys

class Subscriber:
    def __init__(self, id_subscriber):
        self.id_subscriber = id_subscriber
        self.conexion = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.canal = self.conexion.channel()
        self.canal.queue_declare(queue='insult_queue')
        print(f"[Subscriber-{self.id_subscriber}] Iniciado y esperando insultos...")

    def callback(self, ch, method, properties, body):
        insultos = body.decode()
        print(f"[Subscriber-{self.id_subscriber}] Insultos recibidos: {insultos}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def escuchar_insultos(self):
        self.canal.basic_consume(queue='insult_queue',
                                on_message_callback=self.callback,
                                auto_ack=False)
        try:
            self.canal.start_consuming()
        except KeyboardInterrupt:
            print(f"[Subscriber-{self.id_subscriber}] Detenido por teclado.")
            self.cerrar_conexion()

    def cerrar_conexion(self):
        self.canal.close()
        self.conexion.close()

def main():
    if len(sys.argv) < 2:
        print("Uso: python Subscriber.py <id_subscriber>")
        sys.exit(1)
    id_subscriber = sys.argv[1]
    subscriber = Subscriber(id_subscriber)
    subscriber.escuchar_insultos()

if __name__ == "__main__":
    main()
