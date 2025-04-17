import Pyro4

# Establece la conexión con el InsultService
insult_service = Pyro4.Proxy("PYRONAME:insultservice")

# Agregar insultos
insult_service.add_insult("tonto")
insult_service.add_insult("idiota")

# Censura de texto
insult_filter = Pyro4.Proxy("PYRONAME:insultfilter")

result = insult_filter.filter_text("Eres un tonto y un idiota")
print(result)  # Debería imprimir "Eres un CENSORED y un CENSORED"
