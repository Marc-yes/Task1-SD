import Pyro4

@Pyro4.expose
class Subscriber(object):
    def notify(self, insult):
        print(f"[Subscriber] Received insult: {insult}")

def main():
    daemon = Pyro4.Daemon()  # Crea el servidor
    subscriber = Subscriber()  # Crea el objeto Subscriber
    uri = daemon.register(subscriber)  # Registra el objeto
    print(f"Subscriber is running at {uri}")
    
    daemon.requestLoop()  # Mantiene el servicio ejecutándose

if __name__ == "__main__":
    main()
