import csv
import time
import random
import json
from pathlib import Path
from datetime import datetime
import sys
sys.path.append('../')

from libs.common import kafka_manager, get_logger, Topics

class GPSProducer:
    def __init__(self, data_file: str = "../sample_data/gps.csv"):
        self.logger = get_logger("gps_producer")
        self.kafka = kafka_manager
        self.data_file = Path(data_file)
        
    def run(self, loop_forever: bool = True):
        """Run GPS data producer"""
        self.logger.info(f"Starting GPS producer with data from {self.data_file}")
        
        while True:
            try:
                with open(self.data_file, 'r') as f:
                    reader = csv.DictReader(f)
                    
                    for row in reader:
                        # Add current timestamp
                        row['timestamp'] = time.time()
                        
                        # Add some randomness to make it more realistic
                        row['speed_kmph'] = float(row['speed_kmph']) + random.uniform(-2, 2)
                        row['vehicle_count'] = int(row['vehicle_count']) + random.randint(-2, 3)
                        
                        # Ensure non-negative values
                        row['speed_kmph'] = max(0, float(row['speed_kmph']))
                        row['vehicle_count'] = max(1, int(row['vehicle_count']))
                        
                        # Send to Kafka
                        self.kafka.send_message(Topics.GPS_DATA, row, row['segment_id'])
                        
                        self.logger.info(
                            f"Sent GPS data for {row['segment_id']}: "
                            f"speed={row['speed_kmph']:.1f} km/h, "
                            f"vehicles={row['vehicle_count']}"
                        )
                        
                        # Wait between messages
                        time.sleep(random.uniform(0.5, 2.0))
                
                if not loop_forever:
                    break
                    
                self.logger.info("Completed data cycle, restarting...")
                time.sleep(5)  # Pause before restarting
                
            except Exception as e:
                self.logger.error(f"Error in GPS producer: {e}")
                time.sleep(10)

def main():
    producer = GPSProducer()
    producer.run()

if __name__ == "__main__":
    main() 