import Pyro4
import threading
import random
import time

@Pyro4.expose
class InsultService(object):
    def __init__(self):
        self.insults = set()
        self.subscribers = []
        self.running = True
        threading.Thread(target=self._broadcaster, daemon=True).start()

    def add_insult(self, insult):
        if insult not in self.insults:
            print(f"Adding insult: {insult}")
            self.insults.add(insult)
            return True
        return False

    def get_insults(self):
        return list(self.insults)

    def subscribe(self, subscriber_uri):
        print(f"New subscriber: {subscriber_uri}")
        subscriber = Pyro4.Proxy(subscriber_uri)
        self.subscribers.append(subscriber)
        return True

    def _broadcaster(self):
        while self.running:
            if self.insults and self.subscribers:
                insult = random.choice(list(self.insults))
                for sub in self.subscribers:
                    try:
                        sub.notify(insult)
                    except Exception as e:
                        print(f"Subscriber error: {e}")
            time.sleep(5)


def main():
    daemon = Pyro4.Daemon()  # Crea el servidor
    ns = Pyro4.locateNS()  # Conecta al NameServer
    uri = daemon.register(InsultService())  # Registra el objeto
    ns.register("insultservice", uri)  # Registra con el NameServer

    print("InsultService is running.")
    print(f"URI: {uri}")

    daemon.requestLoop()


if __name__ == "__main__":
    main()