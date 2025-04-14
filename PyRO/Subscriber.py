@Pyro5.api.expose
class Subscriber:
    def notify(self, insult):
        print(f"[Subscriber] Received insult: {insult}")