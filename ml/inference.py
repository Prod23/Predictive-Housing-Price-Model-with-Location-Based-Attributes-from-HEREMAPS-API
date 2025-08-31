"""
Real Estate Price Prediction Inference Module
Loads trained model and provides prediction functionality.
"""

import os
import joblib
import numpy as np
import pandas as pd
import logging
from typing import Dict, Union

logger = logging.getLogger(__name__)

class RealEstatePricePredictor:
    """Real estate price prediction model wrapper"""
    
    def __init__(self, artifacts_dir: str = 'artifacts'):
        self.artifacts_dir = artifacts_dir
        self.model = None
        self.scaler = None
        self.location_encoder = None
        self.feature_names = None
        self._load_artifacts()
    
    def _load_artifacts(self):
        """Load all model artifacts"""
        try:
            model_path = os.path.join(self.artifacts_dir, 'model.pkl')
            scaler_path = os.path.join(self.artifacts_dir, 'scaler.pkl')
            encoder_path = os.path.join(self.artifacts_dir, 'location_encoder.pkl')
            features_path = os.path.join(self.artifacts_dir, 'feature_names.pkl')
            
            if not all(os.path.exists(p) for p in [model_path, scaler_path, encoder_path, features_path]):
                raise FileNotFoundError(
                    f"Model artifacts not found in {self.artifacts_dir}. "
                    "Please run 'python ml/train_model.py' first."
                )
            
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.location_encoder = joblib.load(encoder_path)
            self.feature_names = joblib.load(features_path)
            
            logger.info("Model artifacts loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model artifacts: {e}")
            raise
    
    def predict(self, features_dict: Dict[str, Union[int, float]]) -> Dict[str, Union[float, Dict]]:
        """
        Predict house price based on input features
        
        Args:
            features_dict: Dictionary with keys: bhk, sqft, bath, lat, lng
        
        Returns:
            Dictionary with price_crore and features_used
        """
        try:
            # Validate required features
            required_features = ['bhk', 'sqft', 'bath', 'lat', 'lng']
            missing_features = [f for f in required_features if f not in features_dict]
            if missing_features:
                raise ValueError(f"Missing required features: {missing_features}")
            
            # Prepare feature vector
            # Map sqft to total_sqft for consistency with training
            feature_values = {
                'bhk': float(features_dict['bhk']),
                'total_sqft': float(features_dict['sqft']),
                'bath': float(features_dict['bath']),
                'lat': float(features_dict['lat']),
                'lng': float(features_dict['lng']),
                'location_encoded': 0  # Default location encoding for new locations
            }
            
            # Create feature array in the same order as training
            X = np.array([[feature_values[name] for name in self.feature_names]])
            
            # Scale features
            X_scaled = self.scaler.transform(X)
            
            # Make prediction
            price_prediction = self.model.predict(X_scaled)[0]
            
            # Convert to crores (assuming price is in lakhs)
            price_crore = round(price_prediction / 100, 2)
            
            return {
                'price_crore': price_crore,
                'features_used': {
                    'bhk': feature_values['bhk'],
                    'total_sqft': feature_values['total_sqft'],
                    'bath': feature_values['bath'],
                    'lat': feature_values['lat'],
                    'lng': feature_values['lng']
                }
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            raise

def predict(features_dict: Dict[str, Union[int, float]], artifacts_dir: str = 'artifacts') -> Dict:
    """
    Convenience function for making predictions
    
    Args:
        features_dict: Dictionary with keys: bhk, sqft, bath, lat, lng
        artifacts_dir: Path to model artifacts directory
    
    Returns:
        Dictionary with price_crore and features_used
    """
    predictor = RealEstatePricePredictor(artifacts_dir)
    return predictor.predict(features_dict)

# Global predictor instance for Flask app
_predictor = None

def get_predictor(artifacts_dir: str = 'artifacts') -> RealEstatePricePredictor:
    """Get or create global predictor instance"""
    global _predictor
    if _predictor is None:
        _predictor = RealEstatePricePredictor(artifacts_dir)
    return _predictor
