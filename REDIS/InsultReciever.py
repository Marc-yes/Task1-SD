import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0,
decode_responses=True)
pubsub_channel = "events"

# Subscribe to channel
pubsub = client.pubsub()
pubsub.subscribe(pubsub_channel)
print(f"Ets insultat per {pubsub_channel}, waiting for insults...")

# Continuously listen for insults
for insult in pubsub.listen():
    if insult["type"] == "message":
        print(f"Received: {insult['data']}")