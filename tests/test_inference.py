"""
Tests for the ML inference module
"""

import pytest
import os
import sys
import numpy as np
from unittest.mock import patch, MagicMock

# Add parent directory to path to import ml modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ml.inference import RealEstatePricePredictor, predict


class TestRealEstatePricePredictor:
    
    @patch('ml.inference.joblib.load')
    @patch('ml.inference.os.path.exists')
    def test_predictor_initialization_success(self, mock_exists, mock_load):
        """Test successful predictor initialization"""
        mock_exists.return_value = True
        mock_model = MagicMock()
        mock_scaler = MagicMock()
        mock_encoder = MagicMock()
        mock_features = ['bhk', 'total_sqft', 'bath', 'lat', 'lng', 'location_encoded']
        
        mock_load.side_effect = [mock_model, mock_scaler, mock_encoder, mock_features]
        
        predictor = RealEstatePricePredictor('test_artifacts')
        
        assert predictor.model == mock_model
        assert predictor.scaler == mock_scaler
        assert predictor.location_encoder == mock_encoder
        assert predictor.feature_names == mock_features
    
    @patch('ml.inference.os.path.exists')
    def test_predictor_initialization_missing_artifacts(self, mock_exists):
        """Test predictor initialization with missing artifacts"""
        mock_exists.return_value = False
        
        with pytest.raises(FileNotFoundError, match="Model artifacts not found"):
            RealEstatePricePredictor('missing_artifacts')
    
    @patch('ml.inference.joblib.load')
    @patch('ml.inference.os.path.exists')
    def test_predict_success(self, mock_exists, mock_load):
        """Test successful prediction"""
        mock_exists.return_value = True
        
        # Mock model components
        mock_model = MagicMock()
        mock_model.predict.return_value = np.array([150.0])  # Price in lakhs
        
        mock_scaler = MagicMock()
        mock_scaler.transform.return_value = np.array([[1, 2, 3, 4, 5, 6]])
        
        mock_encoder = MagicMock()
        mock_features = ['bhk', 'total_sqft', 'bath', 'lat', 'lng', 'location_encoded']
        
        mock_load.side_effect = [mock_model, mock_scaler, mock_encoder, mock_features]
        
        predictor = RealEstatePricePredictor('test_artifacts')
        
        # Test prediction
        features = {
            'bhk': 3,
            'sqft': 1200,
            'bath': 2,
            'lat': 12.9716,
            'lng': 77.5946
        }
        
        result = predictor.predict(features)
        
        assert 'price_crore' in result
        assert 'features_used' in result
        assert result['price_crore'] == 1.5  # 150 lakhs = 1.5 crores
        assert result['features_used']['bhk'] == 3
        assert result['features_used']['total_sqft'] == 1200
    
    @patch('ml.inference.joblib.load')
    @patch('ml.inference.os.path.exists')
    def test_predict_missing_features(self, mock_exists, mock_load):
        """Test prediction with missing required features"""
        mock_exists.return_value = True
        mock_load.side_effect = [MagicMock(), MagicMock(), MagicMock(), []]
        
        predictor = RealEstatePricePredictor('test_artifacts')
        
        # Missing 'sqft' feature
        features = {
            'bhk': 3,
            'bath': 2,
            'lat': 12.9716,
            'lng': 77.5946
        }
        
        with pytest.raises(ValueError, match="Missing required features"):
            predictor.predict(features)
    
    @patch('ml.inference.RealEstatePricePredictor')
    def test_predict_convenience_function(self, mock_predictor_class):
        """Test the convenience predict function"""
        mock_predictor = MagicMock()
        mock_predictor.predict.return_value = {'price_crore': 2.5}
        mock_predictor_class.return_value = mock_predictor
        
        features = {
            'bhk': 3,
            'sqft': 1500,
            'bath': 2,
            'lat': 12.9716,
            'lng': 77.5946
        }
        
        result = predict(features, 'test_artifacts')
        
        assert result == {'price_crore': 2.5}
        mock_predictor_class.assert_called_once_with('test_artifacts')
        mock_predictor.predict.assert_called_once_with(features)
