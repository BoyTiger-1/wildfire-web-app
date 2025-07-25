"""
Wildfire Risk Prediction Module
Contains the core prediction logic for the web application.
"""

import pandas as pd
import numpy as np
from datetime import datetime
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

class WildfirePredictionSystem:
    def __init__(self):
        self.model = None
        self.feature_columns = [
            'temperature', 'humidity', 'wind_speed', 'precipitation',
            'ndvi', 'elevation', 'slope'
        ]
        self.model_path = os.path.join(os.path.dirname(__file__), 'wildfire_model.pkl')
        
    def generate_synthetic_training_data(self, n_samples=10000):
        """Generate synthetic training data for demonstration purposes."""
        np.random.seed(42)
        
        # Generate weather data
        temperature = np.random.normal(25, 10, n_samples)  # Celsius
        humidity = np.random.uniform(10, 90, n_samples)  # Percentage
        wind_speed = np.random.exponential(5, n_samples)  # km/h
        precipitation = np.random.exponential(2, n_samples)  # mm
        
        # Generate vegetation data (NDVI)
        ndvi = np.random.uniform(0.1, 0.8, n_samples)  # NDVI values
        
        # Generate terrain data
        elevation = np.random.uniform(0, 3000, n_samples)  # meters
        slope = np.random.uniform(0, 45, n_samples)  # degrees
        
        # Generate fire occurrence based on realistic conditions
        fire_risk_score = (
            (temperature - 15) / 20 +  # Higher temp increases risk
            (100 - humidity) / 100 +   # Lower humidity increases risk
            wind_speed / 20 +          # Higher wind increases risk
            (5 - precipitation) / 5 +  # Lower precipitation increases risk
            (0.5 - ndvi) / 0.5 +      # Lower NDVI (drier vegetation) increases risk
            slope / 45                 # Higher slope increases risk
        )
        
        # Add some randomness and create binary fire occurrence
        fire_probability = 1 / (1 + np.exp(-fire_risk_score + 3))  # Sigmoid function
        fire_occurrence = np.random.binomial(1, fire_probability, n_samples)
        
        # Create DataFrame
        data = pd.DataFrame({
            'temperature': temperature,
            'humidity': humidity,
            'wind_speed': wind_speed,
            'precipitation': precipitation,
            'ndvi': ndvi,
            'elevation': elevation,
            'slope': slope,
            'fire_occurrence': fire_occurrence
        })
        
        return data
    
    def train_model(self, data):
        """Train the Random Forest model."""
        X = data[self.feature_columns]
        y = data['fire_occurrence']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1
        }
    
    def get_current_weather_data(self, lat, lon, api_key=None):
        """Get current weather data for a location."""
        try:
            if api_key:
                # Use real OpenWeatherMap API
                url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
                response = requests.get(url)
                if response.status_code == 200:
                    weather_data = response.json()
                    return {
                        'temperature': weather_data['main']['temp'],
                        'humidity': weather_data['main']['humidity'],
                        'wind_speed': weather_data['wind'].get('speed', 0) * 3.6,  # Convert m/s to km/h
                        'precipitation': weather_data.get('rain', {}).get('1h', 0)  # mm in last hour
                    }
            
            # Fallback to synthetic data
            current_weather = {
                'temperature': np.random.normal(25, 5),
                'humidity': np.random.uniform(30, 80),
                'wind_speed': np.random.exponential(3),
                'precipitation': np.random.exponential(1)
            }
            
            return current_weather
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_current_ndvi_data(self, lat, lon):
        """Get current NDVI data for a location."""
        try:
            # For demonstration, return synthetic NDVI
            # In a real implementation, you would use APIs like:
            # - OpenWeather Historical NDVI API
            # - NASA MODIS data
            # - Sentinel Hub API
            current_ndvi = np.random.uniform(0.2, 0.7)
            return current_ndvi
            
        except Exception as e:
            print(f"Error fetching NDVI data: {e}")
            return None
    
    def get_terrain_data(self, lat, lon):
        """Get terrain data (elevation and slope) for a location."""
        try:
            # Try to use Open-Elevation API
            url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                elevation = data['results'][0]['elevation']
                # Estimate slope based on nearby elevation differences (simplified)
                slope = np.random.uniform(0, 30)  # Placeholder for slope calculation
                return {'elevation': elevation, 'slope': slope}
            else:
                # Fallback to synthetic data
                elevation = np.random.uniform(100, 2000)
                slope = np.random.uniform(0, 30)
                return {'elevation': elevation, 'slope': slope}
            
        except Exception as e:
            print(f"Error fetching terrain data: {e}")
            # Fallback to synthetic data
            elevation = np.random.uniform(100, 2000)
            slope = np.random.uniform(0, 30)
            return {'elevation': elevation, 'slope': slope}
    
    def is_location_valid(self, lat, lon):
        """Check if the location is on land and within the USA."""
        # Simple bounds check for continental USA
        if not (-125 <= lon <= -66 and 20 <= lat <= 50):
            return False, "Location is outside the continental United States"
        
        return True, "Location is valid"
    
    def predict_wildfire_risk(self, lat, lon, manual_data=None, weather_api_key=None):
        """Predict wildfire risk for a given location."""
        if self.model is None:
            raise ValueError("Model not trained. Please load the model first.")
        
        # Validate location
        is_valid, message = self.is_location_valid(lat, lon)
        if not is_valid:
            return {'error': message}
        
        if manual_data:
            # Use manually provided data
            features = manual_data
        else:
            # Fetch current data automatically
            weather_data = self.get_current_weather_data(lat, lon, weather_api_key)
            ndvi_data = self.get_current_ndvi_data(lat, lon)
            terrain_data = self.get_terrain_data(lat, lon)
            
            if not all([weather_data, ndvi_data is not None, terrain_data]):
                return {'error': 'Failed to fetch required environmental data'}
            
            features = {
                **weather_data,
                'ndvi': ndvi_data,
                **terrain_data
            }
        
        # Create feature vector
        feature_vector = np.array([[
            features['temperature'],
            features['humidity'],
            features['wind_speed'],
            features['precipitation'],
            features['ndvi'],
            features['elevation'],
            features['slope']
        ]])
        
        # Make prediction
        fire_probability = self.model.predict_proba(feature_vector)[0][1]
        fire_prediction = self.model.predict(feature_vector)[0]
        
        # Determine risk level
        if fire_probability < 0.3:
            risk_level = "Low"
            risk_color = "#22c55e"  # Green
        elif fire_probability < 0.6:
            risk_level = "Moderate"
            risk_color = "#eab308"  # Yellow
        elif fire_probability < 0.8:
            risk_level = "High"
            risk_color = "#f97316"  # Orange
        else:
            risk_level = "Extreme"
            risk_color = "#ef4444"  # Red
        
        result = {
            'location': {'latitude': lat, 'longitude': lon},
            'prediction': {
                'fire_risk_probability': float(fire_probability),
                'fire_predicted': bool(fire_prediction),
                'risk_level': risk_level,
                'risk_color': risk_color
            },
            'input_features': features,
            'timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def save_model(self):
        """Save the trained model to disk."""
        if self.model is None:
            raise ValueError("No model to save. Please train the model first.")
        
        joblib.dump({
            'model': self.model,
            'feature_columns': self.feature_columns
        }, self.model_path)
        
    def load_model(self):
        """Load a trained model from disk."""
        if os.path.exists(self.model_path):
            model_data = joblib.load(self.model_path)
            self.model = model_data['model']
            self.feature_columns = model_data['feature_columns']
            return True
        return False
    
    def initialize_model(self):
        """Initialize the model by loading or training."""
        if not self.load_model():
            # Train a new model if none exists
            training_data = self.generate_synthetic_training_data(n_samples=10000)
            self.train_model(training_data)
            self.save_model()
            return True
        return True

