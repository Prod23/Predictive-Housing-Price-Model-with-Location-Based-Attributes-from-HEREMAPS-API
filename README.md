# Real Estate Price Predictor - Bangalore

## Overview
AI-powered real estate price prediction system for Bangalore properties using location-based attributes and machine learning. Built with Flask backend, HERE Maps integration, and modern web interface.

## Goal
To predict the Real Estate Prices in Bengaluru, India based on Location-based attributes, in a 24 Hour Hackathon
## Approach: 
After researching various property broker sites and talking to experts involved in the real estate industry, we came up with a list of factors on which the price of a property depends:
- Location
- Sq. Ft
- BHK
- No. of Hospitals Nearby
- No. of Parks Nearby
- No. of Schools Nearby
- No. of houses nearby(to determine whether it is a residential area or not)
- No. of Stores Nearby
- No. of Malls Nearby
- No. of Metro Stations Nearby
- No. Of restaurants nearby
## Tech Stack and APIs used
### Backend: 
- Google Colab, Python, ScikitLearn, Pandas, Matplotlib, HERE Search - Forward Geocoder API, HERE Search - Browse API, HERE Maps API,HERE Autosuggest API.
### Frontend:
- HTML, CSS, Javascript


## Model Significance:
- When a person wants to buy a house, they want to look for the availability of hospitals for the wellbeing of their parents/old people and schools for their children.
- A number of restaurants, malls and metro stations in an area means it is a developing area with many commercial spots. 
- As a proxy for future development, we assume places close to maps and restaurants will see greater economic growth and use these parameters to predict prices.
- We define a radius for different parameters.
- For example, a person would need a hospital or school closer to their house than a restaurant. 



## Method:
- Step 1: Scraped the data from Magicbricks website, and saved it in 'household.csv' file
- Step 2: Performed EDA on the dataframe
- Step 3: Using HERE Search - Forward Geocode API from HERE Maps, we found out the (latitude,longitude) coordinate values from text values of each location.
- Step 4: Using HERE Search - Browse API from HERE Maps, we found the different proxies for development like Hospitals, Parks etc. We used different radius for each attribute, like a hospital should be closer to a house than a restaurant, for example. Using this, we will be taking the count for each location.
- Step 5: We then used various models to check for accuracy. We used Linear Regression, KNN Regression, Support Vector Regression, Random Forest Regression and Gradient Boost Regression. In the end, we found maximum accuracy of 70% in Linear Regression. The reason for such a low accuracy is due to shortage of data, as we worked with limited data of 138 datapoints. Due to time constraints of the hackathon, we were encouraged by the HERE Maps team to work on full-fledged implementation of the project.
- Step 6: Created a Javascript-based web application, which used HERE Maps API to interactively display a pin on the map based on the input location address. In the backend, the coordinates are found out for the input location, and based on the other desired inputs from the user for number of bedrooms, bathrooms and Sq. Ft. data, we run a regression along with the other development attributes. We then give the latitude, longitude values and our prediction of the prices.

## Web-app images:

![WhatsApp Image 2023-10-23 at 16 35 59_88c71a5d](https://github.com/Prod23/Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API/assets/86822712/a17e93b3-c9a7-4d3e-bd63-f232a000c981)

![WhatsApp Image 2023-10-23 at 16 36 00_68d5d153](https://github.com/Prod23/Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API/assets/86822712/6ab6b604-e8dc-4609-af82-b45dadd3cd8c)

## Backend/API

### Architecture
- **Flask Backend**: REST API with secure HERE Maps integration
- **ML Pipeline**: Scikit-learn Linear Regression model with feature engineering
- **Database**: CSV-based training data with location geocoding

### API Endpoints
- `POST /api/geocode`: Address to coordinates conversion
- `POST /api/predict`: Price prediction based on property features
- `GET /health`: System health check

## Setup and Installation

### Prerequisites
- Python 3.8+
- HERE Maps API key (free tier available)

### Quick Start

1. **Clone and setup environment**
```bash
git clone <repository-url>
cd Predictive-Housing-Price-Model-with-Location-Based-Attributes-from-HEREMAPS-API
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your HERE_API_KEY
```

3. **Train the model**
```bash
python ml/train_model.py --seed 42
```

4. **Run the application**
```bash
python app.py
# Or using Flask CLI:
FLASK_APP=app.py flask run
```

5. **Access the application**
Open http://localhost:5000 in your browser

### Production Deployment
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Usage

1. Enter a property address in Bangalore
2. Specify BHK, square footage, and number of bathrooms
3. Click "Calculate Price" to get AI-powered price estimate
4. View results on interactive map with location marker

## Testing

Run the test suite:
```bash
pytest tests/ -v
```

## Project Structure
```
├── app.py                 # Flask backend
├── ml/
│   ├── train_model.py     # Model training script
│   └── inference.py       # Prediction module
├── templates/
│   └── index.html         # Frontend template
├── static/
│   ├── css/styles.css     # Styling
│   ├── js/main.js         # Frontend logic
│   └── img/               # Assets
├── tests/                 # Test suite
├── Data/household.csv     # Training data
└── artifacts/             # Generated model files
```

## Verification Checklist

After setup, verify:
- [ ] Model training completes without errors
- [ ] Flask app starts on http://localhost:5000
- [ ] Frontend loads with map display
- [ ] Address geocoding works (updates map marker)
- [ ] Price prediction returns numerical result
- [ ] Tests pass with `pytest -q`

## Future Scope:
- Integrating financial variables such as prevailing interest rates, inflation, employment data to predict whether the pricing is fair or not
- Using Time Series prediction models of house prices to predict whether the investment in the real-estate property is worth it or not
- Enhanced feature engineering with real-time amenity data from HERE Browse API
- Integration with property listing APIs for live market data

