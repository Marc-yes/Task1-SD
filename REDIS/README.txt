Per a que funcioni:
pip install redis

Per als gràfics:
pip install matplotlib

S'ha de activar el servei Redis abans de utilitzar-lo:
redis-server 

Executar InsultProducer.py:
    - Executar InsultProducer.py <Insult>

Executar InsultReciever.py:
    - Executar InsultBroadcaster.py
    - Executar InsultReciever.py

Executar TextProducer.py:
    - Executar InsultFilter.py  
    - Executar TextProducer.py 
    
Executar Service_performance_analysis.py:
    - Executar Service_performance_analysis.py

Executar Filtre_performance_analysis.py:
    - Executar InsultFilter.py
    - Executar Filtre_performance_analysis.py