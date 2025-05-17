import Pyro4
import time

def main():
    # Conectar al NameServer para obtener las URIs de los servicios
    ns = Pyro4.locateNS()
    
    # Obtener la URI de InsultService
    insult_service_uri = ns.lookup("insultservice_1")  # Usar el nombre del nodo de InsultService
    insult_service = Pyro4.Proxy(insult_service_uri)
    
    # Obtener la URI de InsultFilter (el primero de los tres nodos disponibles)
    insult_filter_uri = ns.lookup("insultfilter_1")  # Usar el nombre del nodo de InsultFilter
    insult_service.set_insult_filter(insult_filter_uri)  # Configurar el InsultFilter en el servicio

    # Agregar insultos al InsultService
    insult_service.add_insult("tonto")
    insult_service.add_insult("idiota")
    
    # Enviar los insultos al filtro
    insult_service.pass_insults_to_filter()

    # Probar la filtración de texto usando el InsultFilter
    text_to_filter = "Eres un tonto y un idiota"
    censored_text = insult_service.filter_text(text_to_filter)
    print(f"Filtered text: {censored_text}")
    
    # Agregar un nuevo insulto y pasar a través del filtro nuevamente
    insult_service.add_insult("gilipollas")
    insult_service.pass_insults_to_filter()

    # Ver el resultado filtrado de nuevo
    text_to_filter = "Eres un gilipollas"
    censored_text = insult_service.filter_text(text_to_filter)
    print(f"Filtered text: {censored_text}")
    
    # Esperar un poco para que el servicio continúe enviando insultos
    time.sleep(10)

if __name__ == "__main__":
    main()
