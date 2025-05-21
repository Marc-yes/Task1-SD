import pika
import sys

class InsultFilter:
    def __init__(self, id_nodo):
        self.id_nodo = id_nodo
        self.lista_insultos = []
        self.resultados = []

        self.conexion = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.canal = self.conexion.channel()
        self.canal.queue_declare(queue='insult_queue')
        self.canal.queue_declare(queue='text_queue')
        self.canal.queue_declare(queue='censored_text_queue')

        print(f"[InsultFilter-{self.id_nodo}] Iniciado.")

    def filtrar_texto(self, texto):
        texto_censurado = texto
        for insulto in self.lista_insultos:
            texto_censurado = texto_censurado.replace(insulto, "CENSORED")
        self.resultados.append(texto_censurado)
        #print(f"[InsultFilter-{self.id_nodo}] Texto filtrado: {texto_censurado}")
        return texto_censurado

    def callback_insultos(self, ch, method, properties, body):
        insultos = body.decode()
        self.lista_insultos = insultos.split(",")
        # print(f"[InsultFilter-{self.id_nodo}] Insultos recibidos: {self.lista_insultos}")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def callback_texto(self, ch, method, properties, body):
        texto = body.decode()
        # print(f"[InsultFilter-{self.id_nodo}] Texto recibido: {texto}")
        texto_censurado = self.filtrar_texto(texto)
        self.canal.basic_publish(exchange='',
                                 routing_key='censored_text_queue',
                                 body=texto_censurado)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def comenzar_consumo(self):
        self.canal.basic_consume(queue='insult_queue', on_message_callback=self.callback_insultos)
        self.canal.basic_consume(queue='text_queue', on_message_callback=self.callback_texto)
        print(f"[InsultFilter-{self.id_nodo}] Esperando mensajes...")
        try:
            self.canal.start_consuming()
        except KeyboardInterrupt:
            print(f"[InsultFilter-{self.id_nodo}] Deteniendo...")
            self.conexion.close()

def main():
    if len(sys.argv) < 2:
        print("Uso: python insultfilter.py <id_nodo>")
        sys.exit(1)
    id_nodo = sys.argv[1]
    filtro = InsultFilter(id_nodo)
    filtro.comenzar_consumo()

if __name__ == "__main__":
    main()
