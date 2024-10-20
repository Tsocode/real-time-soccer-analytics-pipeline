import random
import time
from kafka import KafkaProducer
import json

def generate_player_event(player_id):
    """Simulates real-time soccer event data for a player."""
    event_types = ['pass', 'shot', 'goal', 'foul', 'possession']
    event = {
        'player_id': player_id,
        'team': random.choice(['TeamA', 'TeamB']),
        'event_type': random.choice(event_types),
        'location': {'x': random.uniform(0, 100), 'y': random.uniform(0, 100)},
        'time': time.time()
    }
    return event

def simulate_data():
    producer = KafkaProducer(bootstrap_servers='localhost:9092', value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    
    while True:
        for player_id in range(1, 23):  # Simulate for 22 players
            event = generate_player_event(player_id)
            producer.send('soccer-match-events', event)
            print(f"Sent event: {event}")
        time.sleep(1)  # Simulate a delay between events

if __name__ == "__main__":
    simulate_data()
