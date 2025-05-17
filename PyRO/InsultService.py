import Pyro4
import time
import threading
from multiprocessing import Process
import sys

@Pyro4.expose
class InsultService:
    def __init__(self, service_name, insult_filter_uri=None):
        self.insults = set()
        self.subscribers = []
        self.insult_filter_uri = insult_filter_uri
        self.running = True
        self.service_name = service_name
        threading.Thread(target=self._broadcast_insults, daemon=True).start()

    def add_insult(self, insult):
        if insult not in self.insults:
            print(f"[{self.service_name}] Adding insult: {insult}")
            self.insults.add(insult)
            self.pass_insults_to_filter()
            return True
        return False

    def get_insults(self):
        return list(self.insults)

    def subscribe(self, subscriber_uri):
        print(f"[{self.service_name}] New subscriber: {subscriber_uri}")
        subscriber = Pyro4.Proxy(subscriber_uri)
        self.subscribers.append(subscriber)
        return True

    def set_insult_filter(self, insult_filter_uri):
        self.insult_filter_uri = insult_filter_uri
        print(f"[{self.service_name}] Set InsultFilter URI: {self.insult_filter_uri}")

    def pass_insults_to_filter(self):
        if self.insult_filter_uri:
            try:
                insult_filter = Pyro4.Proxy(self.insult_filter_uri)
                insults = self.get_insults()
                insult_filter.receive_insults(insults)
                print(f"[{self.service_name}] Passed insults to filter")
            except Exception as e:
                print(f"[{self.service_name}] Error passing insults to filter: {e}")
        else:
            print(f"[{self.service_name}] No InsultFilter set! Cannot pass insults.")

    def filter_text(self, text):
        if self.insult_filter_uri:
            try:
                insult_filter = Pyro4.Proxy(self.insult_filter_uri)
                censored_text = insult_filter.filter_text(text)
                return censored_text
            except Exception as e:
                print(f"[{self.service_name}] Error filtering text: {e}")
                return text
        else:
            return text

    def _broadcast_insults(self):
        while self.running:
            if self.insults and self.subscribers:
                insult_list = list(self.insults)
                print(f"[{self.service_name}] Sending insult list: {insult_list}")
                for sub in self.subscribers:
                    try:
                        sub.notify(insult_list)
                    except Exception as e:
                        print(f"Subscriber error: {e}")
            else:
                print(f"[{self.service_name}] No insults or no subscribers. Waiting...")
            time.sleep(5)

def run_service(service_name, insult_filter_uri):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    service = InsultService(service_name, insult_filter_uri)
    uri = daemon.register(service)
    ns.register(service_name, uri)

    print(f"{service_name} is running.")
    print(f"URI: {uri}")

    daemon.requestLoop()

def main():
    if len(sys.argv) < 2:
        print("Falta número de nodos. Uso: python InsultService.py <nodos>")
        sys.exit(1)

    try:
        nodes = int(sys.argv[1])
    except ValueError:
        print("El argumento debe ser un número entero.")
        sys.exit(1)

    ns = Pyro4.locateNS()
    procs = []
    for i in range(1, nodes+1):
        service_name = f"insultservice_{i}"
        filter_name = f"insultfilter_{i}"
        try:
            insult_filter_uri = ns.lookup(filter_name)
        except Pyro4.errors.NamingError:
            print(f"No se encontró InsultFilter {filter_name}")
            insult_filter_uri = None

        p = Process(target=run_service, args=(service_name, insult_filter_uri))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

if __name__ == "__main__":
    main()
