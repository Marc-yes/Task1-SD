import Pyro5.api
import threading
import random
import time

# =============================
# InsultService
# =============================

@Pyro5.api.expose
class InsultFilter:
    def __init__(self, insult_service_uri):
        self.results = []
        self.insult_service = Pyro5.api.Proxy(insult_service_uri)

    def filter_text(self, text):
        insults = self.insult_service.get_insults()
        censored_text = text
        for insult in insults:
            censored_text = censored_text.replace(insult, "CENSORED")
        print(f"Filtered text: {censored_text}")
        self.results.append(censored_text)
        return censored_text

    def get_results(self):
        return self.results