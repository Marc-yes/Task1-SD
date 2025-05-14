import Pyro4
import time

def stress_test(insult_services, filter_service, num_operations=100):
    start_time = time.time()

    # Add insults to all insult services
    for insult_service in insult_services:
        insult_service.add_insult("tonto")
        insult_service.add_insult("idiota")

    # Perform text filtering for multiple operations
    text = "Eres un tonto y un idiota"
    for _ in range(num_operations):
        for insult_service in insult_services:
            print(f"Sending text to filter: {text}")
            censored_text = insult_service.filter_text(text)
            print(f"Filtered text: {censored_text}")
    
    elapsed_time = time.time() - start_time
    print(f"Time taken for {num_operations} operations: {elapsed_time} seconds")
    return elapsed_time

def main():
    ns = Pyro4.locateNS()

    # Connect to 1, 2, or 3 InsultService instances
    insult_service_uris = [
        ns.lookup("insultservice_1"),
        ns.lookup("insultservice_2"),
        ns.lookup("insultservice_3")
    ]
    
    insult_services = [Pyro4.Proxy(uri) for uri in insult_service_uris]
    filter_service_uri = ns.lookup("insultfilter")
    filter_service = Pyro4.Proxy(filter_service_uri)

    # Stress test with 3 nodes
    elapsed_time = stress_test(insult_services, filter_service)

if __name__ == "__main__":
    main()
