import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, mean_absolute_error, r2_score
import joblib
import logging
from pathlib import Path
import json
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CongestionModelTrainer:
    def __init__(self, data_path: str = "sample_data/gps.csv"):
        self.data_path = Path(data_path)
        self.model_classifier = None
        self.model_regressor = None
        self.scaler = None
        self.feature_names = None
        
    def load_and_prepare_data(self):
        """Load and prepare training data"""
        logger.info("Loading GPS data...")
        df = pd.read_csv(self.data_path)
        
        # Handle different timestamp formats
        try:
            # Try parsing as Unix timestamp first
            df['hour'] = pd.to_datetime(df['timestamp'], unit='s').dt.hour
            df['day_of_week'] = pd.to_datetime(df['timestamp'], unit='s').dt.dayofweek
        except (ValueError, OSError):
            # If that fails, try parsing as datetime string
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Create derived features
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_rush_hour'] = df['hour'].isin([7, 8, 9, 17, 18, 19]).astype(int)
        
        # Handle weather conditions if present
        if 'weather_condition' in df.columns:
            df['weather_clear'] = (df['weather_condition'] == 'clear').astype(int)
            df['weather_rain'] = (df['weather_condition'] == 'rain').astype(int)
        else:
            df['weather_clear'] = 1
            df['weather_rain'] = 0
        
        # Create congestion classes if not present
        if 'congestion_level' not in df.columns:
            # Calculate congestion based on speed and vehicle count
            expected_speed = 50.0
            df['congestion_level'] = 1.0 - (df['speed_kmph'] / expected_speed) + (df['vehicle_count'] / 50.0) * 0.5
            df['congestion_level'] = df['congestion_level'].clip(0, 1)
        
        # Create congestion categories
        df['congestion_class'] = pd.cut(
            df['congestion_level'], 
            bins=[0, 0.3, 0.7, 1.0], 
            labels=[0, 1, 2],
            include_lowest=True
        ).astype(int)
        
        # Select features for ML
        feature_columns = [
            'speed_kmph', 'vehicle_count', 'hour', 'day_of_week', 
            'is_weekend', 'is_rush_hour', 'weather_clear', 'weather_rain'
        ]
        
        X = df[feature_columns]
        y_class = df['congestion_class']
        y_reg = df['congestion_level']
        
        self.feature_names = feature_columns
        
        return X, y_class, y_reg, df
    
    def train_models(self):
        """Train both classification and regression models"""
        X, y_class, y_reg, df = self.load_and_prepare_data()
        
        # Split data
        X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
            X, y_class, y_reg, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train classification model (congestion levels)
        logger.info("Training classification model...")
        self.model_classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.model_classifier.fit(X_train_scaled, y_class_train)
        
        # Evaluate classification model
        y_class_pred = self.model_classifier.predict(X_test_scaled)
        logger.info("Classification Model Performance:")
        logger.info(f"\n{classification_report(y_class_test, y_class_pred)}")
        
        # Train regression model (congestion score)
        logger.info("Training regression model...")
        self.model_regressor = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42
        )
        self.model_regressor.fit(X_train_scaled, y_reg_train)
        
        # Evaluate regression model
        y_reg_pred = self.model_regressor.predict(X_test_scaled)
        mae = mean_absolute_error(y_reg_test, y_reg_pred)
        r2 = r2_score(y_reg_test, y_reg_pred)
        logger.info(f"Regression Model Performance:")
        logger.info(f"Mean Absolute Error: {mae:.4f}")
        logger.info(f"R² Score: {r2:.4f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': self.feature_names,
            'importance': self.model_classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        logger.info("Feature Importance:")
        logger.info(f"\n{feature_importance}")
        
        return X_test_scaled, y_class_test, y_reg_test
    
    def save_models(self, model_dir: str = "./models"):
        """Save trained models and metadata"""
        model_path = Path(model_dir)
        model_path.mkdir(exist_ok=True)
        
        # Save models
        joblib.dump(self.model_classifier, model_path / "congestion_classifier.pkl")
        joblib.dump(self.model_regressor, model_path / "congestion_regressor.pkl")
        joblib.dump(self.scaler, model_path / "scaler.pkl")
        
        # Save metadata
        metadata = {
            "feature_names": self.feature_names,
            "model_type": "RandomForest",
            "trained_on": datetime.now().isoformat(),
            "congestion_levels": {
                "0": "Free Flow",
                "1": "Moderate",
                "2": "Heavy", 
                "3": "Severe"
            }
        }
        
        with open(model_path / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Models saved to {model_path}")
    
    def load_models(self, model_dir: str = "./models"):
        """Load trained models"""
        model_path = Path(model_dir)
        
        self.model_classifier = joblib.load(model_path / "congestion_classifier.pkl")
        self.model_regressor = joblib.load(model_path / "congestion_regressor.pkl")
        self.scaler = joblib.load(model_path / "scaler.pkl")
        
        with open(model_path / "metadata.json", "r") as f:
            metadata = json.load(f)
            self.feature_names = metadata["feature_names"]
        
        logger.info("Models loaded successfully")
    
    def predict_congestion(self, features: dict) -> dict:
        """Predict congestion for given features"""
        if self.model_classifier is None or self.model_regressor is None:
            raise ValueError("Models not trained or loaded")
        
        # Prepare feature vector
        feature_vector = np.array([[features.get(name, 0) for name in self.feature_names]])
        feature_vector_scaled = self.scaler.transform(feature_vector)
        
        # Predictions
        congestion_level = self.model_classifier.predict(feature_vector_scaled)[0]
        congestion_score = self.model_regressor.predict(feature_vector_scaled)[0]
        congestion_proba = self.model_classifier.predict_proba(feature_vector_scaled)[0]
        
        # Confidence (max probability)
        confidence = float(np.max(congestion_proba))
        
        level_names = ["Free Flow", "Moderate", "Heavy", "Severe"]
        
        return {
            "congestion_level": int(congestion_level),
            "congestion_level_name": level_names[congestion_level],
            "congestion_score": float(congestion_score),
            "confidence": confidence,
            "probabilities": {
                level_names[i]: float(prob) for i, prob in enumerate(congestion_proba)
            }
        }

def main():
    """Main training function"""
    trainer = CongestionModelTrainer()
    
    # Train models
    trainer.train_models()
    
    # Save models
    trainer.save_models()
    
    # Test prediction
    test_features = {
        'speed_kmph': 25.0,
        'vehicle_count': 30,
        'vehicle_density': 1.2,
        'hour': 8,
        'day_of_week': 1,
        'is_weekend': 0,
        'is_rush_hour': 1
    }
    
    prediction = trainer.predict_congestion(test_features)
    logger.info(f"Test prediction: {prediction}")

if __name__ == "__main__":
    main() 