# Wildfire Risk Prediction System

A web-based wildfire risk prediction system powered by machine learning that provides real-time wildfire risk assessment for locations within the continental United States.

## Inspiration
Two years ago, my community was reminded of how close we all are to the devastating impacts of wildfires. A massive fire had broken out near a town just an hour away from us. For days, the air was thick with smoke, evacuation alerts loomed, and my family and neighbors prepared in case we had to leave our homes behind. Although we were fortunate not to evacuate, the fear and uncertainty left a lasting impression on me. Furthermore, the LA wildfires erupted with terrifying intensity, destroying entire neighborhoods, displacing thousands of families, and showing how quickly a spark can lead to a disaster. Seeing these events happen so close to home, I realized that climate change and wildfire risk are not distant issues, but they’re immediate, life-altering threats. This inspired me to act, to use the skills I’m developing in artificial intelligence and data science to create something meaningful. By building a Wildfire Risk Prediction AI, I want to contribute to early detection and prevention, helping communities prepare before it’s too late. My goal is to turn the anxiety and helplessness of those moments into something constructive, with technology that empowers people and protects lives.


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
## Technology Stack

- **Machine Learning**: Random Forest Classifier (scikit-learn)
- **Backend**: Python
- **Frontend**: HTML/CSS/JavaScript
- **Key Libraries**: scikit-learn, pandas, NumPy, Geopy, Requests
- **Deployment**: Render
- **Data Sources**: NASA FIRMS (real-time), Synthetic Data (training), USGS Elevation Data

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

## Usage

- Access the web interface at https://wildfire-web-app.onrender.com
- Enter location coordinates (latitude/longitude) or use the map to select coordinates
- Adjust environmental parameters or use current conditions
- Click "Predict" to generate wildfire risk percentage
- View results on interactive map

### Risk Levels

- **Low** (< 30%): Green indicator
- **Moderate** (30-60%): Yellow indicator  
- **High** (60-80%): Orange indicator
- **Extreme** (> 80%): Red indicator

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


