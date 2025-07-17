import os
import json
import requests
import logging
from azure.eventhub import EventHubProducerClient, EventData
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

# Configurations
CTA_API_KEY = os.getenv("CTA_API_KEY")
EVENT_HUB_CONN_STR = os.getenv("EVENT_HUB_CONN_STR")
EVENT_HUB_NAME = "bus-data"

def main(mytimer: func.TimerRequest) -> None:
    # Get bus positions for all routes
    vehicles = get_bus_positions()
    
    if vehicles:
        send_to_eventhub(vehicles)
        logging.info(f"Sent {len(vehicles)} bus events")
    else:
        logging.warning("No bus data received")

def get_bus_positions():
    try:
        url = f"https://ctabustracker.com/bustime/api/v2/getvehicles?key={CTA_API_KEY}&format=json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data["bustime-response"]["vehicle"]
    except Exception as e:
        logging.error(f"API Error: {str(e)}")
        return []

def send_to_eventhub(vehicles):
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENT_HUB_CONN_STR,
        eventhub_name=EVENT_HUB_NAME
    )
    
    try:
        batch = producer.create_batch()
        for bus in vehicles:
            # Add timestamp and enrich data
            bus["processed_time"] = datetime.utcnow().isoformat()
            
            # Convert to Event Data
            event = EventData(json.dumps(bus))
            batch.add(event)
        
        producer.send_batch(batch)
    finally:
        producer.close()

# Test locally
if __name__ == "__main__":
    mock_timer = type('obj', (object,), {'past_due': False})
    main(mock_timer)