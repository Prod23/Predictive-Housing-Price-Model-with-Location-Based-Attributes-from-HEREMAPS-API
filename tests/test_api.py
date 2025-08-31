"""
Tests for the Flask API endpoints
"""

import pytest
import json
import sys
import os
from unittest.mock import patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestAPI:
    
    def test_index_route(self, client):
        """Test the index route returns HTML"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Real Estate Price Predictor' in response.data
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'status' in data
        assert 'model_loaded' in data
        assert 'here_api_configured' in data
    
    @patch('app.requests.get')
    @patch('app.HERE_API_KEY', 'test_key')
    def test_geocode_success(self, mock_get, client):
        """Test successful geocoding"""
        # Mock HERE API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'items': [{
                'position': {'lat': 12.9716, 'lng': 77.5946},
                'title': 'Bangalore, India'
            }]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = client.post('/api/geocode',
                             data=json.dumps({'q': 'Bangalore'}),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'lat' in data
        assert 'lng' in data
        assert data['lat'] == 12.9716
        assert data['lng'] == 77.5946
    
    @patch('app.HERE_API_KEY', 'test_key')
    def test_geocode_missing_query(self, client):
        """Test geocoding with missing query"""
        response = client.post('/api/geocode',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('app.HERE_API_KEY', 'test_key')
    def test_geocode_empty_query(self, client):
        """Test geocoding with empty query"""
        response = client.post('/api/geocode',
                             data=json.dumps({'q': ''}),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('app.requests.get')
    @patch('app.HERE_API_KEY', 'test_key')
    def test_geocode_address_not_found(self, mock_get, client):
        """Test geocoding when address is not found"""
        mock_response = MagicMock()
        mock_response.json.return_value = {'items': []}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = client.post('/api/geocode',
                             data=json.dumps({'q': 'nonexistent address'}),
                             content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    @patch('app.predictor')
    def test_predict_success(self, mock_predictor, client):
        """Test successful price prediction"""
        mock_predictor.predict.return_value = {
            'price_crore': 2.5,
            'features_used': {
                'bhk': 3,
                'total_sqft': 1200,
                'bath': 2,
                'lat': 12.9716,
                'lng': 77.5946
            }
        }
        
        payload = {
            'bhk': 3,
            'sqft': 1200,
            'bath': 2,
            'lat': 12.9716,
            'lng': 77.5946
        }
        
        response = client.post('/api/predict',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'price_crore' in data
        assert data['price_crore'] == 2.5
    
    def test_predict_missing_fields(self, client):
        """Test prediction with missing required fields"""
        payload = {
            'bhk': 3,
            'sqft': 1200
            # Missing bath, lat, lng
        }
        
        response = client.post('/api/predict',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing required fields' in data['error']
    
    def test_predict_invalid_bhk(self, client):
        """Test prediction with invalid BHK value"""
        payload = {
            'bhk': 15,  # Too high
            'sqft': 1200,
            'bath': 2,
            'lat': 12.9716,
            'lng': 77.5946
        }
        
        response = client.post('/api/predict',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_predict_invalid_coordinates(self, client):
        """Test prediction with invalid coordinates"""
        payload = {
            'bhk': 3,
            'sqft': 1200,
            'bath': 2,
            'lat': 50.0,  # Outside Bangalore region
            'lng': 77.5946
        }
        
        response = client.post('/api/predict',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_predict_no_json_body(self, client):
        """Test prediction without JSON body"""
        response = client.post('/api/predict')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_404_endpoint(self, client):
        """Test 404 handler"""
        response = client.get('/nonexistent')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
