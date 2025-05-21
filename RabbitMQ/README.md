Es necesario que el servidor rabbit este iniciado: sudo systemctl start rabbitmq-server

Si se quiere ejecutar el script de demostración: python demo.py
A partir de aqui es recomenable comentar la linea 23 de InsultFilter.py que imprimeix per pantalla els textos censurats.

Executar stress_client: python stress_client [nombre_textos]

Executar subscriptor: 
    -python3 InsultService.py [id_node]
    -python3 Subscriber.py [id_node]
Es important que el id sigui el mateix, si es vol afegir un altre subscriptor bastaria amb tornar a executar Subscriber.py amb el mateix id.