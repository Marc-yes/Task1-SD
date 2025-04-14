import Pyro5.api
import threading
import random
import time

# =============================
# InsultService
# =============================

@Pyro5.api.expose
class InsultService:
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
        subscriber = Pyro5.api.Proxy(subscriber_uri)
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