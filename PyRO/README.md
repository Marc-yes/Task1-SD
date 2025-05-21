Per a que funcioni Pyro:
pyro4-ns

Per veure el funcionament del programa podeu executar directament: python demo.py
A partir de aqui es recomenable comentar la linea 23 de InsultFilter.py que imprime por pantalla los textos censurados.

Per executar el stress_client:
1r pas: Executar InsultFilter < python InsultFilter.py [nombre_nodes] >
2n pas: Executar InsultService < python InsultService.py [nombre_nodes] >
3r pas: Executar test de rendiment < stress_client [nombre_textos] >

Per executar el Subscriber:
1r pas: Executar InsultService < python InsultService.py [nombre_nodes] >
2n pas: Executar Subscriber < python Subscriber.py >

