import Pyro4
import sys
from multiprocessing import Process

@Pyro4.expose
class InsultFilter:
    def __init__(self, name):
        self.name = name
        self.insults = ["idiota"]
        self.resultados = []

    def receive_insults(self, insult_list):
        self.insults = insult_list
        print(f"[{self.name}] Insultos recibidos: {self.insults}")

    def filter_text(self, text):
        filtered = text
        for insult in self.insults:
            filtered = filtered.replace(insult, "CENSORED")
        print(f"[{self.name}] Texto filtrado: {filtered}")
        self.resultados.append(filtered)

        return filtered

def run_filter(name):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()

    obj = InsultFilter(name)
    uri = daemon.register(obj)
    ns.register(name, uri)

    print(f"{name} running at {uri}")
    daemon.requestLoop()

def main():
    if len(sys.argv) < 2:
        print("Uso: python InsultFilter.py <nodos>")
        sys.exit(1)

    nodes = int(sys.argv[1])
    procs = []
    for i in range(1, nodes+1):
        name = f"insultfilter_{i}"
        p = Process(target=run_filter, args=(name,))
        p.start()
        procs.append(p)

    for p in procs:
        p.join()

if __name__ == "__main__":
    main()
