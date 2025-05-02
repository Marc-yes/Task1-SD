import xmlrpc.client

# Crear client per connectar-se a InsultServer
s = xmlrpc.client.ServerProxy('http://localhost:8005')

# Afegir insults
print(s.add_insult("sorra"))
print(s.add_insult("tonto"))
print(s.add_insult("cretino"))

# Obtenir insults
print(s.get_insults())

# Subscripció al servei per rebre insults aleatoris
#subscriber_url = "http://localhost:8004"  # URL del servidor InsultFilter
#print(s.subscribe(subscriber_url))

# Llistar mètodes disponibles
print(s.system.listMethods())
