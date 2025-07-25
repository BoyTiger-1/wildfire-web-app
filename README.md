# Wildfire Risk Prediction System

A web-based wildfire risk prediction system powered by machine learning that provides real-time wildfire risk assessment for locations within the continental United States.

## Features

- **Location Input**: Enter coordinates manually or select locations on an interactive map
- **Automatic Data Fetching**: Automatically retrieves current weather, vegetation, and terrain data
- **Manual Data Input**: Option to manually input environmental parameters for custom scenarios
- **Risk Assessment**: Provides wildfire risk probability with color-coded risk levels (Low, Moderate, High, Extreme)
- **Responsive Design**: Works on both desktop and mobile devices
- **Real-time Predictions**: Instant predictions using a trained Random Forest model

## System Requirements

- Python 3.11+
- Flask web framework
- Required Python packages (see requirements.txt)

## Installation

1. **Extract the application files** to your desired directory
2. **Navigate to the application directory**:
   ```bash
   cd wildfire-web-app
   ```
3. **Activate the virtual environment**:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies** (if not already installed):
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### API Keys (Optional)

For real-time weather data, you can configure the following API keys:

1. **OpenWeatherMap API Key** (for weather data):
   - Sign up at https://openweathermap.org/api
   - Set the environment variable: `export OPENWEATHER_API_KEY=your_api_key`
   - Or provide it through the web interface

2. **NASA FIRMS MAP_KEY** (for fire data):
   - Request at https://firms.modaps.eosdis.nasa.gov/api/map_key/
   - Set the environment variable: `export FIRMS_MAP_KEY=your_map_key`

**Note**: The system works without API keys using synthetic data for demonstration purposes.

## Running the Application

1. **Start the Flask server**:
   ```bash
   python src/main.py
   ```

2. **Access the application**:
   - Open your web browser
   - Navigate to `http://localhost:5000`

3. **Using the application**:
   - Enter latitude and longitude coordinates (e.g., 34.0522, -118.2437 for Los Angeles)
   - Choose between automatic data fetching or manual input
   - Click "Predict Wildfire Risk" to get the assessment

## API Endpoints

The application provides REST API endpoints:

- `POST /api/wildfire/predict` - Predict wildfire risk with automatic data fetching
- `POST /api/wildfire/predict-manual` - Predict wildfire risk with manual data input
- `GET /api/wildfire/health` - Health check endpoint

### Example API Usage

```bash
# Automatic prediction
curl -X POST http://localhost:5000/api/wildfire/predict \
  -H "Content-Type: application/json" \
  -d '{"latitude": 34.0522, "longitude": -118.2437}'

# Manual prediction
curl -X POST http://localhost:5000/api/wildfire/predict-manual \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 34.0522,
    "longitude": -118.2437,
    "temperature": 35,
    "humidity": 15,
    "wind_speed": 25,
    "precipitation": 0,
    "ndvi": 0.2,
    "elevation": 500,
    "slope": 15
  }'
```

## Model Information

The system uses a Random Forest classifier trained on synthetic data that considers:

- **Weather factors**: Temperature, humidity, wind speed, precipitation
- **Vegetation factors**: NDVI (Normalized Difference Vegetation Index)
- **Terrain factors**: Elevation and slope

### Risk Levels

- **Low** (< 30%): Green indicator
- **Moderate** (30-60%): Yellow indicator  
- **High** (60-80%): Orange indicator
- **Extreme** (> 80%): Red indicator

## File Structure

```
wildfire-web-app/
├── src/
│   ├── main.py                 # Flask application entry point
│   ├── wildfire_predictor.py   # Core prediction logic
│   ├── routes/
│   │   ├── wildfire.py         # API routes for predictions
│   │   └── user.py             # User management routes
│   ├── models/
│   │   └── user.py             # Database models
│   └── static/
│       ├── index.html          # Frontend interface
│       ├── styles.css          # Styling
│       └── script.js           # Frontend JavaScript
├── venv/                       # Virtual environment
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Deployment

For production deployment:

1. **Use a production WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
   ```

2. **Configure a reverse proxy** (nginx, Apache) for better performance

3. **Set up SSL/TLS** for secure connections

4. **Configure environment variables** for API keys

## Limitations

- **Demonstration System**: Uses synthetic training data for demonstration purposes
- **Geographic Scope**: Limited to continental United States coordinates
- **Data Sources**: For production use, integrate real historical weather, vegetation, and fire occurrence data
- **Model Accuracy**: The current model is trained on synthetic data and should be retrained with real data for production use

## Troubleshooting

### Common Issues

1. **"Failed to fetch" error**: Check that the Flask server is running and accessible
2. **Invalid coordinates**: Ensure latitude is between -90 and 90, longitude between -180 and 180
3. **Location outside USA**: The system only accepts coordinates within the continental United States
4. **Missing dependencies**: Run `pip install -r requirements.txt` to install all required packages

### Development

To modify or extend the system:

1. **Backend changes**: Edit files in `src/` directory
2. **Frontend changes**: Modify files in `src/static/` directory
3. **Model improvements**: Update `wildfire_predictor.py` with new features or algorithms
4. **API extensions**: Add new routes in `src/routes/` directory

## License

This is a demonstration system created for educational purposes.

## Support

For issues or questions about the system, please refer to the code comments and documentation within the source files.

