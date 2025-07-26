import threading
import time
import sys
sys.path.append('../')

from libs.common import get_logger
from gps_producer import GPSProducer
from weather_producer import WeatherProducer
from events_producer import EventsProducer

def main():
    logger = get_logger("ingestion_service")
    logger.info("Starting all data producers...")
    
    # Initialize producers
    gps_producer = GPSProducer()
    weather_producer = WeatherProducer()
    events_producer = EventsProducer()
    
    # Create threads for each producer
    threads = [
        threading.Thread(target=gps_producer.run, daemon=True, name="GPS-Producer"),
        threading.Thread(target=weather_producer.run, daemon=True, name="Weather-Producer"),
        threading.Thread(target=events_producer.run, daemon=True, name="Events-Producer")
    ]
    
    # Start all threads
    for thread in threads:
        thread.start()
        logger.info(f"Started {thread.name}")
        time.sleep(2)  # Stagger startup
    
    logger.info("All producers started successfully")
    
    try:
        # Keep main thread alive
        while True:
            # Check if any thread died
            for thread in threads:
                if not thread.is_alive():
                    logger.error(f"Thread {thread.name} died!")
            
            time.sleep(30)
            
    except KeyboardInterrupt:
        logger.info("Shutting down ingestion service...")

if __name__ == "__main__":
    main() 