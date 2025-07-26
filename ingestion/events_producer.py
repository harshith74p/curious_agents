import json
import time
import random
from pathlib import Path
from datetime import datetime
import sys
sys.path.append('../')

from libs.common import kafka_manager, get_logger, Topics

class EventsProducer:
    def __init__(self, events_file: str = "../sample_data/events.json"):
        self.logger = get_logger("events_producer")
        self.kafka = kafka_manager
        self.events_file = Path(events_file)
        
    def run(self, loop_forever: bool = True):
        """Run traffic events producer"""
        self.logger.info(f"Starting Events producer with data from {self.events_file}")
        
        while True:
            try:
                with open(self.events_file, 'r') as f:
                    events = json.load(f)
                
                for event in events:
                    # Update timestamp to current time
                    current_time = time.time()
                    event['start_time'] = current_time
                    
                    # Calculate end time based on estimated duration
                    if 'estimated_duration' in event:
                        event['end_time'] = current_time + event['estimated_duration']
                    
                    # Add some randomness to severity and description
                    if random.random() < 0.1:  # 10% chance to modify severity
                        severities = ['low', 'medium', 'high', 'critical']
                        current_idx = severities.index(event['severity'])
                        # Move severity up or down by 1 level
                        new_idx = max(0, min(len(severities)-1, current_idx + random.choice([-1, 1])))
                        event['severity'] = severities[new_idx]
                    
                    # Send to Kafka
                    self.kafka.send_message(Topics.TRAFFIC_EVENTS, event, event['event_id'])
                    
                    self.logger.info(
                        f"Sent event {event['event_id']}: "
                        f"{event['event_type']} - {event['severity']} severity"
                    )
                    
                    # Random delay between events
                    time.sleep(random.uniform(30, 120))
                
                if not loop_forever:
                    break
                    
                self.logger.info("Completed events cycle, restarting...")
                time.sleep(300)  # Wait 5 minutes before restarting
                
            except Exception as e:
                self.logger.error(f"Error in events producer: {e}")
                time.sleep(60)

def main():
    producer = EventsProducer()
    producer.run()

if __name__ == "__main__":
    main() 