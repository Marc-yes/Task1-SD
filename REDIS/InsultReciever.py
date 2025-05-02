import redis

# Connect to Redis
client = redis.Redis(host='localhost', port=6379, db=0,
decode_responses=True)
pubsub_channel = "pubsub_channel"

# Subscribe to channel
pubsub = client.pubsub()
pubsub.subscribe(channel_name)
print(f"Ets insultat per {channel_name}, waiting for insults...")

# Continuously listen for insults
for insult in pubsub.listen():
    if insult["type"] == "message":
        print(f"Received: {insult['data']}")