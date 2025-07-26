import asyncio
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import numpy as np
import pandas as pd
from dataclasses import asdict
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib

# Import from shared libraries
import sys
sys.path.append('../')
from libs.common import (
    get_logger, kafka_manager, redis_manager, 
    Topics, RedisKeys, dataclass_to_dict
)

class RootCauseScorer:
    def __init__(self):
        self.logger = get_logger("root_cause_scorer")
        self.kafka = kafka_manager
        self.redis = redis_manager
        self.model = None
        self.scaler = None
        self.feature_names = [
            'speed_kmph', 'vehicle_count', 'vehicle_density',
            'hour', 'day_of_week', 'is_weekend', 'is_rush_hour',
            'precipitation', 'visibility', 'event_severity', 'incident_nearby'
        ]
        self._load_or_train_model()

    def _load_or_train_model(self):
        try:
            self.model = joblib.load("./root_cause_model.pkl")
            self.scaler = joblib.load("./root_cause_scaler.pkl")
            self.logger.info("Loaded root cause model from disk.")
        except Exception:
            self.logger.warning("No pre-trained model found. Training a new one with mock data.")
            self._train_mock_model()

    def _train_mock_model(self):
        # Generate mock data for demonstration
        np.random.seed(42)
        n = 200
        X = pd.DataFrame({
            'speed_kmph': np.random.uniform(5, 80, n),
            'vehicle_count': np.random.randint(5, 60, n),
            'vehicle_density': np.random.uniform(0.1, 3.0, n),
            'hour': np.random.randint(0, 24, n),
            'day_of_week': np.random.randint(0, 7, n),
            'is_weekend': np.random.randint(0, 2, n),
            'is_rush_hour': np.random.randint(0, 2, n),
            'precipitation': np.random.uniform(0, 5, n),
            'visibility': np.random.uniform(2, 10, n),
            'event_severity': np.random.randint(0, 4, n),
            'incident_nearby': np.random.randint(0, 2, n)
        })
        # 0: normal, 1: weather, 2: event, 3: incident
        y = np.random.choice([0, 1, 2, 3], n, p=[0.5, 0.2, 0.2, 0.1])
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.model.fit(X_scaled, y)
        joblib.dump(self.model, "./root_cause_model.pkl")
        joblib.dump(self.scaler, "./root_cause_scaler.pkl")
        self.logger.info("Trained and saved mock root cause model.")

    def _extract_features(self, congestion_data: Dict, context_data: Dict = None) -> np.ndarray:
        # Extract features from congestion and context
        features = {
            'speed_kmph': congestion_data.get('avg_speed', 30),
            'vehicle_count': congestion_data.get('vehicle_count', 20),
            'vehicle_density': congestion_data.get('vehicle_density', 1.0),
            'hour': congestion_data.get('hour', 8),
            'day_of_week': congestion_data.get('day_of_week', 2),
            'is_weekend': congestion_data.get('is_weekend', 0),
            'is_rush_hour': congestion_data.get('is_rush_hour', 1),
            'precipitation': 0.0,
            'visibility': 10.0,
            'event_severity': 0,
            'incident_nearby': 0
        }
        if context_data:
            weather = context_data.get('weather_conditions', {})
            features['precipitation'] = weather.get('precipitation', 0.0)
            features['visibility'] = weather.get('visibility', 10.0)
            # Event severity: 0-none, 1-low, 2-medium, 3-high
            events = context_data.get('events', [])
            if events:
                sev_map = {'low': 1, 'medium': 2, 'high': 3, 'critical': 3}
                features['event_severity'] = max([sev_map.get(e.get('impact_level', 'low'), 1) for e in events])
            # Incident nearby
            alerts = context_data.get('traffic_alerts', [])
            features['incident_nearby'] = int(any(a.get('type') in ['accident', 'incident'] for a in alerts))
        return np.array([[features[k] for k in self.feature_names]])

    def score_root_cause(self, congestion_data: Dict, context_data: Dict = None) -> Dict:
        features = self._extract_features(congestion_data, context_data)
        features_scaled = self.scaler.transform(features)
        proba = self.model.predict_proba(features_scaled)[0]
        cause_idx = int(np.argmax(proba))
        cause_names = ['normal', 'weather', 'event', 'incident']
        return {
            'root_cause': cause_names[cause_idx],
            'probabilities': {cause_names[i]: float(proba[i]) for i in range(len(cause_names))},
            'features': {k: float(features[0][i]) for i, k in enumerate(self.feature_names)}
        }

    async def process_congestion_alerts(self):
        self.logger.info("Starting root cause scoring for congestion alerts...")
        consumer = self.kafka.get_consumer([Topics.CONGESTION_ALERTS], "root_cause_scorer_group")
        for message in consumer:
            try:
                alert_data = message.value
                segment_id = alert_data.get('segment_id')
                # Get context for this segment
                segment_data = self.redis.get_json(f"segment:{segment_id}")
                context_data = self.redis.get_json(RedisKeys.CONTEXT_CACHE.format(location=f"{segment_data.get('latitude')},{segment_data.get('longitude')}")) if segment_data else None
                # Score root cause
                result = self.score_root_cause(alert_data, context_data)
                # Publish to Kafka or cache
                self.kafka.send_message(Topics.ROOT_CAUSE, {**alert_data, 'root_cause': result['root_cause'], 'root_cause_probabilities': result['probabilities']}, segment_id)
                self.logger.info(f"Scored root cause for {segment_id}: {result['root_cause']}")
            except Exception as e:
                self.logger.error(f"Error scoring root cause: {e}")
                continue

    def score_from_api(self, congestion_data: Dict, context_data: Dict = None) -> Dict:
        return self.score_root_cause(congestion_data, context_data) 