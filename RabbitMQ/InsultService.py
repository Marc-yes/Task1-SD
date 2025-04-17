import pika
import random
import time

# Connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare a queue where insults will be published
channel.queue_declare(queue='insult_queue')

class InsultService:
    def __init__(self):
        self.insults = set()
        self.running = True
        print("InsultService started...")
        self.broadcast_insults()

    def add_insult(self, insult):
        if insult not in self.insults:
            self.insults.add(insult)
            print(f"Insult added: {insult}")
            return True
        return False

    def get_insults(self):
        return list(self.insults)

    def broadcast_insults(self):
        while self.running:
            if self.insults:
                insult = random.choice(list(self.insults))
                # Publish a random insult to the queue
                channel.basic_publish(exchange='',
                                      routing_key='insult_queue',
                                      body=insult)
                print(f"[InsultService] Sent insult: {insult}")
            time.sleep(5)

# Start the InsultService
if __name__ == '__main__':
    service = InsultService()
