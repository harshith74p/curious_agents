import csv
import time
import random
import json
from pathlib import Path
from datetime import datetime
import sys
sys.path.append('../')

from libs.common import kafka_manager, get_logger, Topics

class WeatherProducer:
    def __init__(self, data_file: str = "../sample_data/weather.csv"):
        self.logger = get_logger("weather_producer")
        self.kafka = kafka_manager
        self.data_file = Path(data_file)
        
    def run(self, loop_forever: bool = True):
        """Run weather data producer"""
        self.logger.info(f"Starting Weather producer with data from {self.data_file}")
        
        while True:
            try:
                with open(self.data_file, 'r') as f:
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        # Add current timestamp
                        row['timestamp'] = time.time()
                        
                        # Add some randomness for realistic weather changes
                        row['temperature'] = float(row['temperature']) + random.uniform(-1, 1)
                        row['humidity'] = float(row['humidity']) + random.uniform(-5, 5)
                        row['wind_speed'] = float(row['wind_speed']) + random.uniform(-2, 2)
                        row['precipitation'] = max(0, float(row['precipitation']) + random.uniform(-0.5, 0.5))
                        row['visibility'] = float(row['visibility']) + random.uniform(-1, 1)
                        
                        # Ensure realistic ranges
                        row['humidity'] = max(0, min(100, float(row['humidity'])))
                        row['wind_speed'] = max(0, float(row['wind_speed']))
                        row['visibility'] = max(0.1, min(20, float(row['visibility'])))
                        
                        # Create location key
                        location_key = f"{row['latitude']},{row['longitude']}"
                        
                        # Send to Kafka
                        self.kafka.send_message(Topics.WEATHER_DATA, row, location_key)
                        
                        self.logger.info(
                            f"Sent weather data for {location_key}: "
                            f"temp={row['temperature']:.1f}°C, "
                            f"precip={row['precipitation']:.1f}mm, "
                            f"visibility={row['visibility']:.1f}km"
                        )
                        
                        # Weather updates less frequently
                        time.sleep(random.uniform(10, 30))
                
                if not loop_forever:
                    break
                    
                self.logger.info("Completed weather cycle, restarting...")
                time.sleep(60)  # Wait a minute before restarting
                
            except Exception as e:
                self.logger.error(f"Error in weather producer: {e}")
                time.sleep(30)

def main():
    producer = WeatherProducer()
    producer.run()

if __name__ == "__main__":
    main() 