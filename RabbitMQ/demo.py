import subprocess
import time
import pika

def enviar_texto(texto):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='text_queue')
    channel.basic_publish(exchange='', routing_key='text_queue', body=texto)
    print(f"[Demo] Texto enviado: {texto}")
    connection.close()

def main():
    # Lanzar insultservice.py y insultfilter.py como procesos hijos
    proc_service = subprocess.Popen(['python3', 'InsultService.py', '1'])
    proc_filter = subprocess.Popen(['python3', 'InsultFilter.py', '1'])

    try:
        # Esperamos un poco para que los servicios arranquen y envíen insultos
        time.sleep(6)

        # Ahora enviamos textos para censurar
        textos = [
            "Eres un idiota y un estúpido.",
            "Qué día tan tonto.",
            "No eres imbécil, solo cansado.",
            "Nada malo aquí."
        ]

        for texto in textos:
            enviar_texto(texto)
            time.sleep(6)  # Esperar a que el filtro procese

        # Opcional: Leer los textos censurados desde la cola censored_text_queue
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='censored_text_queue')
        print("\n[Demo] Textos censurados recibidos:")

        while True:
            method_frame, header_frame, body = channel.basic_get(queue='censored_text_queue', auto_ack=True)
            if method_frame:
                print(body.decode())
            else:
                break
        connection.close()

    except KeyboardInterrupt:
        pass
    finally:
        # Terminar los procesos hijos
        proc_service.terminate()
        proc_filter.terminate()
        proc_service.wait()
        proc_filter.wait()
        print("[Demo] Servicios detenidos.")

if __name__ == "__main__":
    main()
