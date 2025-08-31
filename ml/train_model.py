#!/usr/bin/env python3
"""
Real Estate Price Prediction Model Training
Loads household.csv, performs feature engineering, and trains a Linear Regression model.
"""

import argparse
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_and_preprocess_data(data_path: str, seed: int = 42):
    """Load and preprocess the household data"""
    logger.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)
    
    # Basic data cleaning
    df = df.dropna(subset=['price', 'total_sqft', 'bath'])
    
    # Extract BHK from size column
    df['bhk'] = df['size'].str.extract('(\d+)').astype(float)
    df = df.dropna(subset=['bhk'])
    
    # Clean total_sqft - handle ranges by taking average
    def clean_sqft(x):
        if pd.isna(x):
            return np.nan
        if isinstance(x, str):
            if '-' in x:
                parts = x.split('-')
                try:
                    return (float(parts[0]) + float(parts[1])) / 2
                except:
                    return np.nan
            else:
                try:
                    return float(x)
                except:
                    return np.nan
        return float(x)
    
    df['total_sqft'] = df['total_sqft'].apply(clean_sqft)
    df = df.dropna(subset=['total_sqft'])
    
    # Add dummy lat/lng for locations (in production, these would come from HERE API)
    # For now, use Bangalore center with small random variations
    np.random.seed(seed)
    df['lat'] = 12.9716 + np.random.normal(0, 0.1, len(df))
    df['lng'] = 77.5946 + np.random.normal(0, 0.1, len(df))
    
    # Encode location for additional features
    location_encoder = LabelEncoder()
    df['location_encoded'] = location_encoder.fit_transform(df['location'].fillna('Unknown'))
    
    logger.info(f"Data shape after preprocessing: {df.shape}")
    return df, location_encoder

def prepare_features(df):
    """Prepare feature matrix and target vector"""
    # Select features for the model
    feature_cols = ['bhk', 'total_sqft', 'bath', 'lat', 'lng', 'location_encoded']
    X = df[feature_cols].copy()
    y = df['price'].copy()
    
    # Remove outliers (simple approach)
    Q1 = y.quantile(0.25)
    Q3 = y.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    mask = (y >= lower_bound) & (y <= upper_bound)
    X = X[mask]
    y = y[mask]
    
    logger.info(f"Features shape after outlier removal: {X.shape}")
    return X, y

def train_model(X, y, seed=42):
    """Train the Linear Regression model"""
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    logger.info(f"Model Performance:")
    logger.info(f"  MAE: {mae:.2f}")
    logger.info(f"  R²: {r2:.3f}")
    
    return model, scaler, mae, r2

def save_artifacts(model, scaler, location_encoder, feature_names, artifacts_dir):
    """Save model and preprocessing artifacts"""
    os.makedirs(artifacts_dir, exist_ok=True)
    
    # Save model
    model_path = os.path.join(artifacts_dir, 'model.pkl')
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")
    
    # Save scaler
    scaler_path = os.path.join(artifacts_dir, 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    logger.info(f"Scaler saved to {scaler_path}")
    
    # Save location encoder
    encoder_path = os.path.join(artifacts_dir, 'location_encoder.pkl')
    joblib.dump(location_encoder, encoder_path)
    logger.info(f"Location encoder saved to {encoder_path}")
    
    # Save feature names
    features_path = os.path.join(artifacts_dir, 'feature_names.pkl')
    joblib.dump(feature_names, features_path)
    logger.info(f"Feature names saved to {features_path}")

def main():
    parser = argparse.ArgumentParser(description='Train real estate price prediction model')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for reproducibility')
    parser.add_argument('--data-path', type=str, default='Data/household.csv', 
                       help='Path to household data CSV')
    parser.add_argument('--artifacts-dir', type=str, default='artifacts',
                       help='Directory to save model artifacts')
    
    args = parser.parse_args()
    
    # Load and preprocess data
    df, location_encoder = load_and_preprocess_data(args.data_path, args.seed)
    
    # Prepare features
    X, y = prepare_features(df)
    feature_names = list(X.columns)
    
    # Train model
    model, scaler, mae, r2 = train_model(X, y, args.seed)
    
    # Save artifacts
    save_artifacts(model, scaler, location_encoder, feature_names, args.artifacts_dir)
    
    logger.info("Training completed successfully!")
    logger.info(f"Final model performance: MAE={mae:.2f}, R²={r2:.3f}")

if __name__ == '__main__':
    main()
