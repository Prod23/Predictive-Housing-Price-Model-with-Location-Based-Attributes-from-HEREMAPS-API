#!/usr/bin/env python3
"""
Flask backend for Real Estate Price Prediction
Provides REST API endpoints for geocoding and price prediction.
"""

import os
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import logging
from ml.inference import get_predictor

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
HERE_API_KEY = os.getenv('HERE_API_KEY')
HERE_MAPS_JS_KEY = os.getenv('HERE_MAPS_JS_KEY')
if not HERE_API_KEY:
    logger.warning("HERE_API_KEY not found in environment variables")

# Initialize predictor
try:
    predictor = get_predictor()
    logger.info("Model predictor initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize predictor: {e}")
    predictor = None

@app.route('/')
def index():
    """Serve the main application page"""
    return render_template('index.html', here_maps_js_key=HERE_MAPS_JS_KEY)

@app.route('/api/geocode', methods=['POST'])
def geocode():
    """
    Geocode an address using HERE API
    
    Request JSON: { "q": "address string" }
    Response JSON: { "lat": float, "lng": float, "raw": {...} }
    """
    try:
        if not HERE_API_KEY:
            return jsonify({
                'error': 'HERE API key not configured'
            }), 500
        
        data = request.get_json()
        if not data or 'q' not in data:
            return jsonify({
                'error': 'Missing required field: q (address query)'
            }), 400
        
        address_query = data['q'].strip()
        if not address_query:
            return jsonify({
                'error': 'Address query cannot be empty'
            }), 400
        
        # Call HERE Geocoding API
        url = "https://geocode.search.hereapi.com/v1/geocode"
        params = {
            'apiKey': HERE_API_KEY,
            'q': address_query,
            'limit': 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        if not response.ok:
            logger.error(f"HERE geocode error {response.status_code}: {response.text}")
            try:
                err_json = response.json()
            except Exception:
                err_json = {'message': response.text}
            return jsonify({
                'error': 'Geocoding failed',
                'details': err_json,
                'status_code': response.status_code
            }), 503
        response.raise_for_status()
        
        geocode_data = response.json()
        
        if not geocode_data.get('items'):
            return jsonify({
                'error': 'Address not found'
            }), 404
        
        # Extract coordinates from first result
        location = geocode_data['items'][0]['position']
        
        return jsonify({
            'lat': location['lat'],
            'lng': location['lng'],
            'raw': geocode_data['items'][0]
        })
        
    except requests.exceptions.RequestException as e:
        logger.error(f"HERE API request failed: {e}")
        return jsonify({
            'error': 'Geocoding service unavailable'
        }), 503
    except Exception as e:
        logger.error(f"Geocoding error: {e}")
        return jsonify({
            'error': 'Internal server error'
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """
    Predict house price based on features
    
    Request JSON: { "bhk": int, "sqft": float, "bath": int, "lat": float, "lng": float }
    Response JSON: { "price_crore": float, "features_used": {...} }
    """
    try:
        if not predictor:
            return jsonify({
                'error': 'Prediction model not available. Please train the model first.'
            }), 503
        
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'Request body must be JSON'
            }), 400
        
        # Validate required fields
        required_fields = ['bhk', 'sqft', 'bath', 'lat', 'lng']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'error': f'Missing required fields: {missing_fields}'
            }), 400
        
        # Validate field types and ranges
        try:
            bhk = int(data['bhk'])
            sqft = float(data['sqft'])
            bath = int(data['bath'])
            lat = float(data['lat'])
            lng = float(data['lng'])
            
            # Basic validation
            if bhk < 1 or bhk > 10:
                return jsonify({'error': 'BHK must be between 1 and 10'}), 400
            if sqft < 100 or sqft > 10000:
                return jsonify({'error': 'Square feet must be between 100 and 10000'}), 400
            if bath < 1 or bath > 10:
                return jsonify({'error': 'Bathrooms must be between 1 and 10'}), 400
            if not (10 <= lat <= 15) or not (75 <= lng <= 80):
                return jsonify({'error': 'Coordinates must be within Bangalore region'}), 400
                
        except (ValueError, TypeError) as e:
            return jsonify({
                'error': 'Invalid field types. BHK and bath must be integers, sqft/lat/lng must be numbers'
            }), 400
        
        # Make prediction
        features = {
            'bhk': bhk,
            'sqft': sqft,
            'bath': bath,
            'lat': lat,
            'lng': lng
        }
        
        result = predictor.predict(features)
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({
            'error': 'Prediction failed'
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'here_api_configured': HERE_API_KEY is not None,
        'here_maps_js_configured': HERE_MAPS_JS_KEY is not None
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create artifacts directory if it doesn't exist
    os.makedirs('artifacts', exist_ok=True)
    
    # Run the app
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
