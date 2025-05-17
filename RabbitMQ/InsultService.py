import pika
import time
import sys

class InsultService:
    def __init__(self, id_nodo):
        self.id_nodo = id_nodo
        self.insultos = {"tonto", "idiota", "imbécil", "estúpido"}
        self.ejecutando = True
        self.conexion = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.canal = self.conexion.channel()
        self.canal.queue_declare(queue='insult_queue')
        self.canal.queue_declare(queue='text_queue')
        print(f"[InsultService-{self.id_nodo}] Iniciado.")

    def transmitir_insultos(self):
        while self.ejecutando:
            if self.insultos:
                mensaje = ",".join(self.insultos)
                self.canal.basic_publish(exchange='',
                                         routing_key='insult_queue',
                                         body=mensaje)
                print(f"[InsultService-{self.id_nodo}] Insultos enviados: {mensaje}")
            time.sleep(5)

    def enviar_texto(self, texto):
        self.canal.basic_publish(exchange='',
                                 routing_key='text_queue',
                                 body=texto)
        print(f"[InsultService-{self.id_nodo}] Texto enviado: {texto}")

    def cerrar_conexion(self):
        self.conexion.close()

def main():
    if len(sys.argv) < 2:
        print("Uso: python insultservice.py <id_nodo>")
        sys.exit(1)
    id_nodo = sys.argv[1]
    servicio = InsultService(id_nodo)

    try:
        servicio.transmitir_insultos()
    except KeyboardInterrupt:
        print(f"[InsultService-{id_nodo}] Deteniendo...")
        servicio.ejecutando = False
        servicio.cerrar_conexion()

if __name__ == "__main__":
    main()
