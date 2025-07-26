// Wildfire Risk Prediction System - Frontend JavaScript

class WildfirePredictionApp {
    constructor() {
        this.map = null;
        this.selectedMarker = null;
        this.isManualData = false;
        this.isMapMode = false;
        
        this.initializeEventListeners();
        this.initializeMap();
    }

    initializeEventListeners() {
        // Input method toggle
        document.getElementById('coordsBtn').addEventListener('click', () => this.toggleInputMethod('coords'));
        document.getElementById('mapBtn').addEventListener('click', () => this.toggleInputMethod('map'));
        
        // Data method toggle
        document.getElementById('autoDataBtn').addEventListener('click', () => this.toggleDataMethod('auto'));
        document.getElementById('manualDataBtn').addEventListener('click', () => this.toggleDataMethod('manual'));
        
        // Predict button
        document.getElementById('predictBtn').addEventListener('click', () => this.makePrediction());
        
        // Enter key support for inputs
        const inputs = document.querySelectorAll('input[type="number"]');
        inputs.forEach(input => {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.makePrediction();
                }
            });
        });
    }

    initializeMap() {
        // Initialize Leaflet map centered on the US
        this.map = L.map('map').setView([39.8283, -98.5795], 4);
        
        // Add OpenStreetMap tiles
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);
        
        // Add click event to map
        this.map.on('click', (e) => {
            this.selectLocationOnMap(e.latlng.lat, e.latlng.lng);
        });
    }

    toggleInputMethod(method) {
        const coordsBtn = document.getElementById('coordsBtn');
        const mapBtn = document.getElementById('mapBtn');
        const coordsInput = document.getElementById('coordsInput');
        const mapInput = document.getElementById('mapInput');
        
        if (method === 'coords') {
            coordsBtn.classList.add('active');
            mapBtn.classList.remove('active');
            coordsInput.classList.remove('hidden');
            mapInput.classList.add('hidden');
            this.isMapMode = false;
        } else {
            mapBtn.classList.add('active');
            coordsBtn.classList.remove('active');
            mapInput.classList.remove('hidden');
            coordsInput.classList.add('hidden');
            this.isMapMode = true;
            
            // Invalidate map size when switching to map mode
            setTimeout(() => {
                this.map.invalidateSize();
            }, 100);
        }
    }

    toggleDataMethod(method) {
        const autoBtn = document.getElementById('autoDataBtn');
        const manualBtn = document.getElementById('manualDataBtn');
        const manualDataInput = document.getElementById('manualDataInput');
        
        if (method === 'auto') {
            autoBtn.classList.add('active');
            manualBtn.classList.remove('active');
            manualDataInput.classList.add('hidden');
            this.isManualData = false;
        } else {
            manualBtn.classList.add('active');
            autoBtn.classList.remove('active');
            manualDataInput.classList.remove('hidden');
            this.isManualData = true;
        }
    }

    selectLocationOnMap(lat, lng) {
        // Remove existing marker
        if (this.selectedMarker) {
            this.map.removeLayer(this.selectedMarker);
        }
        
        // Add new marker
        this.selectedMarker = L.marker([lat, lng]).addTo(this.map);
        
        // Update coordinate inputs
        document.getElementById('latitude').value = lat.toFixed(6);
        document.getElementById('longitude').value = lng.toFixed(6);
    }

    getCoordinates() {
        const lat = parseFloat(document.getElementById('latitude').value);
        const lon = parseFloat(document.getElementById('longitude').value);
        
        if (isNaN(lat) || isNaN(lon)) {
            throw new Error('Please enter valid latitude and longitude values');
        }
        
        if (lat < -90 || lat > 90) {
            throw new Error('Latitude must be between -90 and 90');
        }
        
        if (lon < -180 || lon > 180) {
            throw new Error('Longitude must be between -180 and 180');
        }
        
        return { latitude: lat, longitude: lon };
    }

    getManualData() {
        const fields = ['temperature', 'humidity', 'windSpeed', 'precipitation', 'ndvi', 'elevation', 'slope'];
        const data = {};
        
        for (const field of fields) {
            const value = parseFloat(document.getElementById(field).value);
            if (isNaN(value)) {
                throw new Error(`Please enter a valid value for ${field.replace(/([A-Z])/g, ' $1').toLowerCase()}`);
            }
            
            // Convert windSpeed to wind_speed for API compatibility
            const apiField = field === 'windSpeed' ? 'wind_speed' : field;
            data[apiField] = value;
        }
        
        // Validate ranges
        if (data.humidity < 0 || data.humidity > 100) {
            throw new Error('Humidity must be between 0 and 100');
        }
        
        if (data.ndvi < 0 || data.ndvi > 1) {
            throw new Error('NDVI must be between 0 and 1');
        }
        
        if (data.wind_speed < 0) {
            throw new Error('Wind speed cannot be negative');
        }
        
        if (data.precipitation < 0) {
            throw new Error('Precipitation cannot be negative');
        }
        
        if (data.elevation < 0) {
            throw new Error('Elevation cannot be negative');
        }
        
        if (data.slope < 0 || data.slope > 90) {
            throw new Error('Slope must be between 0 and 90 degrees');
        }
        
        return data;
    }

    async makePrediction() {
        const predictBtn = document.getElementById('predictBtn');
        const btnText = document.querySelector('.btn-text');
        const spinner = document.querySelector('.loading-spinner');
        const resultsContainer = document.getElementById('resultsContainer');
        const errorContainer = document.getElementById('errorContainer');
        
        try {
            // Hide previous results
            resultsContainer.classList.add('hidden');
            errorContainer.classList.add('hidden');
            
            // Show loading state
            predictBtn.disabled = true;
            btnText.textContent = 'Predicting...';
            spinner.classList.remove('hidden');
            
            // Get coordinates
            const coordinates = this.getCoordinates();
            
            // Prepare request data
             // Prepare request data
            let requestData = {
                latitude: coordinates.latitude,
                longitude: coordinates.longitude
            };
            
            // Add manual data if selected
            if (this.isManualData) {
                const manualData = this.getManualData();
                // For manual endpoint, merge manual data directly into request
                requestData = { ...requestData, ...manualData };
            }
            
            // Make API request
            const endpoint = this.isManualData ? '/api/wildfire/predict-manual' : '/api/wildfire/predict';
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Prediction failed');
            }
            
            // Display results
            this.displayResults(result);
            
        } catch (error) {
            this.displayError(error.message);
        } finally {
            // Reset button state
            predictBtn.disabled = false;
            btnText.textContent = 'Predict Wildfire Risk';
            spinner.classList.add('hidden');
        }
    }

    displayResults(result) {
        const resultsContainer = document.getElementById('resultsContainer');
        const prediction = result.prediction;
        const features = result.input_features;
        const location = result.location;
        
        // Update risk level and indicator
        const riskLevel = document.getElementById('riskLevel');
        const riskIndicator = document.getElementById('riskIndicator');
        const riskProbability = document.getElementById('riskProbability');
        
        riskLevel.textContent = prediction.risk_level;
        riskLevel.style.color = prediction.risk_color;
        riskIndicator.style.backgroundColor = prediction.risk_color;
        riskProbability.textContent = (prediction.fire_risk_probability * 100).toFixed(1) + '%';
        
        // Update location info
        document.getElementById('resultCoords').textContent = 
            `${location.latitude.toFixed(4)}, ${location.longitude.toFixed(4)}`;
        document.getElementById('predictionTime').textContent = 
            new Date(result.timestamp).toLocaleString();
        
        // Update environmental data
        document.getElementById('dataTemp').textContent = `${features.temperature.toFixed(1)}°C`;
        document.getElementById('dataHumidity').textContent = `${features.humidity.toFixed(1)}%`;
        document.getElementById('dataWind').textContent = `${features.wind_speed.toFixed(1)} km/h`;
        document.getElementById('dataPrecip').textContent = `${features.precipitation.toFixed(1)} mm`;
        document.getElementById('dataNdvi').textContent = features.ndvi.toFixed(3);
        document.getElementById('dataElevation').textContent = `${features.elevation.toFixed(0)} m`;
        document.getElementById('dataSlope').textContent = `${features.slope.toFixed(1)}°`;
        
        // Show results
        resultsContainer.classList.remove('hidden');
        
        // Scroll to results
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    displayError(message) {
        const errorContainer = document.getElementById('errorContainer');
        const errorMessage = document.getElementById('errorMessage');
        
        errorMessage.textContent = message;
        errorContainer.classList.remove('hidden');
        
        // Scroll to error
        errorContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Initialize the application when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new WildfirePredictionApp();
});

// Add some example locations for quick testing
const exampleLocations = [
    { name: 'Los Angeles, CA', lat: 34.0522, lon: -118.2437 },
    { name: 'Phoenix, AZ', lat: 33.4484, lon: -112.0740 },
    { name: 'Denver, CO', lat: 39.7392, lon: -104.9903 },
    { name: 'Portland, OR', lat: 45.5152, lon: -122.6784 },
    { name: 'Austin, TX', lat: 30.2672, lon: -97.7431 }
];

// Add example location buttons (optional enhancement)
function addExampleLocations() {
    const inputPanel = document.querySelector('.input-panel');
    const exampleDiv = document.createElement('div');
    exampleDiv.className = 'example-locations';
    exampleDiv.innerHTML = '<h3>Quick Examples</h3>';
    
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'example-buttons';
    buttonContainer.style.cssText = 'display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;';
    
    exampleLocations.forEach(location => {
        const button = document.createElement('button');
        button.textContent = location.name;
        button.className = 'example-btn';
        button.style.cssText = 'padding: 8px 12px; border: 1px solid #ddd; background: white; border-radius: 6px; cursor: pointer; font-size: 0.9rem;';
        
        button.addEventListener('click', () => {
            document.getElementById('latitude').value = location.lat;
            document.getElementById('longitude').value = location.lon;
        });
        
        buttonContainer.appendChild(button);
    });
    
    exampleDiv.appendChild(buttonContainer);
    inputPanel.appendChild(exampleDiv);
}

