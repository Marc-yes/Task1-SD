import Pyro4
import threading
import time

from InsultService import InsultService
from InsultFilter import InsultFilter

def start_filter(stop_event):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    filter_obj = InsultFilter("insultfilter_1")
    uri = daemon.register(filter_obj)
    ns.register("insultfilter_1", uri)
    print("InsultFilter_1 running at:", uri)

    def loop():
        daemon.requestLoop()

    t = threading.Thread(target=loop)
    t.start()

    stop_event.wait()
    daemon.shutdown()
    t.join()
    print("Filter daemon stopped")

def start_service(insult_filter_uri, stop_event):
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    service_obj = InsultService("insultservice_1", insult_filter_uri)
    uri = daemon.register(service_obj)
    ns.register("insultservice_1", uri)
    print("InsultService_1 running at:", uri)

    def loop():
        daemon.requestLoop()

    t = threading.Thread(target=loop)
    t.start()

    stop_event.wait()
    daemon.shutdown()
    t.join()
    print("Service daemon stopped")

def main():
    stop_event = threading.Event()

    filter_thread = threading.Thread(target=start_filter, args=(stop_event,))
    filter_thread.start()
    time.sleep(1)

    ns = Pyro4.locateNS()
    insult_filter_uri = ns.lookup("insultfilter_1")

    service_thread = threading.Thread(target=start_service, args=(insult_filter_uri, stop_event))
    service_thread.start()
    time.sleep(1)

    insult_service = Pyro4.Proxy(ns.lookup("insultservice_1"))

    insult_service.add_insult("tonto")
    insult_service.pass_insults_to_filter()
    censored = insult_service.filter_text("Eres un tonto")
    print("Texto filtrado:", censored)

    stop_event.set()
    filter_thread.join()
    service_thread.join()

    print("Demo terminada, nodos cerrados.")

if __name__ == "__main__":
    main()
