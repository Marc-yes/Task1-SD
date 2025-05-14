import redis

# Conectar a Redis
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

r.spop('insult_list', r.scard('insult_list'))