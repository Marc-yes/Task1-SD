import Pyro5.api
import threading
import random
import time

def main():
    daemon = Pyro5.api.Daemon()

    insult_service = InsultService()
    insult_uri = daemon.register(insult_service)
    print(f"InsultService ready at {insult_uri}")

    insult_filter = InsultFilter(insult_uri)
    filter_uri = daemon.register(insult_filter)
    print(f"InsultFilter ready at {filter_uri}")

    subscriber = Subscriber()
    subscriber_uri = daemon.register(subscriber)
    print(f"Subscriber ready at {subscriber_uri}")

    insult_service.subscribe(subscriber_uri)

    daemon.requestLoop()


if __name__ == "__main__":
    main()
