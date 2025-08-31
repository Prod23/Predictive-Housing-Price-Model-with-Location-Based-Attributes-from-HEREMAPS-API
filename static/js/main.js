// Real Estate Price Predictor - Main JavaScript

class RealEstatePredictor {
    constructor() {
        this.map = null;
        this.marker = null;
        this.currentLocation = null;
        this.initializeMap();
        this.bindEvents();
    }

    initializeMap() {
        // Initialize HERE Maps platform using injected key from template
        const jsKey = (window && window.HERE_MAPS_JS_KEY) ? window.HERE_MAPS_JS_KEY.trim() : '';
        if (!jsKey) {
            console.error('HERE Maps JS key is not configured. Set HERE_MAPS_JS_KEY in your .env');
            this.showError('Map cannot load: HERE Maps JS key not configured.');
            return;
        }
        const platform = new H.service.Platform({ apikey: jsKey });

        const defaultLayers = platform.createDefaultLayers();

        // Initialize map centered on Bangalore
        this.map = new H.Map(
            document.getElementById('mapContainer'),
            defaultLayers.raster.normal.map,
            {
                center: { lat: 12.9716, lng: 77.5946 },
                zoom: 12,
                pixelRatio: window.devicePixelRatio || 1
            }
        );

        // Enable map interaction
        const behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(this.map));
        const ui = H.ui.UI.createDefault(this.map, defaultLayers);

        // Handle window resize
        window.addEventListener('resize', () => this.map.getViewPort().resize());
    }

    bindEvents() {
        const form = document.getElementById('priceForm');
        form.addEventListener('submit', (e) => this.handleFormSubmit(e));
    }

    async handleFormSubmit(event) {
        event.preventDefault();
        
        const address = document.getElementById('address').value.trim();
        const bhk = parseInt(document.getElementById('bhk').value);
        const sqft = parseFloat(document.getElementById('sqft').value);
        const bath = parseInt(document.getElementById('bath').value);

        if (!address || !bhk || !sqft || !bath) {
            this.showError('Please fill in all fields');
            return;
        }

        this.showLoading(true);
        this.hideResults();
        this.hideError();

        try {
            // Step 1: Geocode the address
            const locationData = await this.geocodeAddress(address);
            
            // Step 2: Update map with location
            this.updateMapLocation(locationData);
            
            // Step 3: Get price prediction
            const prediction = await this.predictPrice({
                bhk: bhk,
                sqft: sqft,
                bath: bath,
                lat: locationData.lat,
                lng: locationData.lng
            });
            
            // Step 4: Display results
            this.showResults(prediction, locationData, address);
            
        } catch (error) {
            console.error('Prediction error:', error);
            this.showError(error.message || 'Failed to calculate price estimate');
        } finally {
            this.showLoading(false);
        }
    }

    async geocodeAddress(address) {
        const response = await fetch('/api/geocode', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ q: address })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to find address');
        }

        return await response.json();
    }

    async predictPrice(features) {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(features)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to predict price');
        }

        return await response.json();
    }

    updateMapLocation(locationData) {
        const { lat, lng } = locationData;
        
        // Remove existing marker if any
        if (this.marker) {
            this.map.removeObject(this.marker);
        }

        // Create new marker with custom icon
        const icon = new H.map.Icon('/static/img/Drawing-Pin.png', { size: { w: 56, h: 56 } });
        this.marker = new H.map.Marker({ lat, lng }, { icon });
        
        // Add marker to map
        this.map.addObject(this.marker);
        
        // Center map on location
        this.map.setCenter({ lat, lng });
        this.map.setZoom(15);
        
        this.currentLocation = { lat, lng };
    }

    showResults(prediction, locationData, address) {
        const resultsDiv = document.getElementById('results');
        const priceResultDiv = document.getElementById('priceResult');
        const locationResultDiv = document.getElementById('locationResult');

        priceResultDiv.innerHTML = `
            <div>Estimated Price: <span style="color: #28a745;">₹${prediction.price_crore} Crores</span></div>
        `;

        locationResultDiv.innerHTML = `
            <div><strong>Location:</strong> ${address}</div>
            <div><strong>Coordinates:</strong> ${locationData.lat.toFixed(4)}, ${locationData.lng.toFixed(4)}</div>
            <div><strong>Features Used:</strong> ${prediction.features_used.bhk} BHK, ${prediction.features_used.total_sqft} sq ft, ${prediction.features_used.bath} bathrooms</div>
        `;

        resultsDiv.style.display = 'block';
    }

    showLoading(show) {
        const loadingDiv = document.getElementById('loading');
        loadingDiv.style.display = show ? 'block' : 'none';
    }

    hideResults() {
        const resultsDiv = document.getElementById('results');
        resultsDiv.style.display = 'none';
    }

    showError(message) {
        const errorDiv = document.getElementById('error');
        const errorMessageDiv = document.getElementById('errorMessage');
        
        errorMessageDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    hideError() {
        const errorDiv = document.getElementById('error');
        errorDiv.style.display = 'none';
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new RealEstatePredictor();
});
