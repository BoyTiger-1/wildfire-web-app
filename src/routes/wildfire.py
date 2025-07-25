"""
Wildfire prediction API routes
"""

from flask import Blueprint, request, jsonify
from src.wildfire_predictor import WildfirePredictionSystem
import os

wildfire_bp = Blueprint('wildfire', __name__)

# Initialize the prediction system
predictor = WildfirePredictionSystem()
predictor.initialize_model()

@wildfire_bp.route('/predict', methods=['POST'])
def predict_wildfire_risk():
    """Predict wildfire risk for a given location."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract coordinates
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid latitude or longitude format'}), 400
        
        # Check if manual data is provided
        manual_data = data.get('manual_data')
        
        # Get weather API key from environment or request
        weather_api_key = os.environ.get('OPENWEATHER_API_KEY') or data.get('weather_api_key')
        
        # Make prediction
        result = predictor.predict_wildfire_risk(
            lat=lat,
            lon=lon,
            manual_data=manual_data,
            weather_api_key=weather_api_key
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@wildfire_bp.route('/predict-manual', methods=['POST'])
def predict_wildfire_risk_manual():
    """Predict wildfire risk using manually provided environmental data."""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Extract coordinates
        lat = data.get('latitude')
        lon = data.get('longitude')
        
        if lat is None or lon is None:
            return jsonify({'error': 'Latitude and longitude are required'}), 400
        
        try:
            lat = float(lat)
            lon = float(lon)
        except (ValueError, TypeError):
            return jsonify({'error': 'Invalid latitude or longitude format'}), 400
        
        # Extract manual environmental data
        required_fields = ['temperature', 'humidity', 'wind_speed', 'precipitation', 'ndvi', 'elevation', 'slope']
        manual_data = {}
        
        for field in required_fields:
            value = data.get(field)
            if value is None:
                return jsonify({'error': f'Missing required field: {field}'}), 400
            
            try:
                manual_data[field] = float(value)
            except (ValueError, TypeError):
                return jsonify({'error': f'Invalid value for {field}'}), 400
        
        # Make prediction
        result = predictor.predict_wildfire_risk(
            lat=lat,
            lon=lon,
            manual_data=manual_data
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@wildfire_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor.model is not None,
        'timestamp': predictor.model is not None
    }), 200

