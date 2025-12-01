"""
Modeling utilities for sales forecasting
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class SalesForecaster:
    def __init__(self, model_type='random_forest'):
        """
        Initialize the sales forecaster
        
        Parameters:
        model_type (str): Type of model to use ('random_forest', 'linear_regression')
        """
        self.model_type = model_type
        if model_type == 'random_forest':
            self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        elif model_type == 'linear_regression':
            self.model = LinearRegression()
        else:
            raise ValueError("Unsupported model type. Use 'random_forest' or 'linear_regression'")
            
        self.is_trained = False
        self.scaler = StandardScaler()
        
    def prepare_data_for_training(self, df, target_col='sales', test_size=0.2):
        """Prepare data for training the model"""
        # Select only numeric columns for modeling
        numeric_df = df.select_dtypes(include=[np.number])
        
        if target_col not in numeric_df.columns:
            raise ValueError(f"Target column '{target_col}' not found in data")
            
        # Separate features and target
        X = numeric_df.drop(columns=[target_col])
        y = numeric_df[target_col]
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        return X_train, X_test, y_train, y_test
    
    def train(self, X_train, y_train):
        """Train the forecasting model"""
        # Scale the features for linear regression
        if self.model_type == 'linear_regression':
            X_train = self.scaler.fit_transform(X_train)
            
        self.model.fit(X_train, y_train)
        self.is_trained = True
        return self
    
    def predict(self, X):
        """Make predictions with the trained model"""
        if not self.is_trained:
            raise ValueError("Model must be trained before making predictions")
            
        # Scale the features for linear regression
        if self.model_type == 'linear_regression':
            X = self.scaler.transform(X)
            
        return self.model.predict(X)
    
    def evaluate(self, X_test, y_test):
        """Evaluate model performance"""
        if not self.is_trained:
            raise ValueError("Model must be trained before evaluation")
            
        # Scale the features for linear regression
        if self.model_type == 'linear_regression':
            X_test_scaled = self.scaler.transform(X_test)
            y_pred = self.predict(X_test_scaled)
        else:
            y_pred = self.predict(X_test)
            
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_test, y_pred)
        
        return {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2': r2
        }
    
    def get_feature_importance(self, feature_names):
        """Get feature importance (for tree-based models)"""
        if not self.is_trained:
            raise ValueError("Model must be trained before getting feature importance")
            
        if self.model_type == 'random_forest':
            importance = self.model.feature_importances_
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': importance
            }).sort_values('importance', ascending=False)
            return feature_importance
        else:
            # For linear regression, we can use coefficients
            coefficients = self.model.coef_
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'coefficient': coefficients
            }).sort_values('coefficient', key=abs, ascending=False)
            return feature_importance

class TimeSeriesForecaster:
    """Simple time series forecaster using moving averages"""
    
    def __init__(self, window=7):
        self.window = window
        
    def fit(self, ts_data, target_col='sales'):
        """Fit the forecaster (store historical data)"""
        self.historical_data = ts_data.copy()
        self.target_col = target_col
        return self
    
    def predict(self, steps=30):
        """Generate forecasts for future periods"""
        # Simple moving average forecast
        last_values = self.historical_data[self.target_col].tail(self.window).values
        forecast_value = np.mean(last_values)
        
        # Generate forecast dates
        last_date = self.historical_data['date'].max()
        forecast_dates = [last_date + pd.Timedelta(days=i) for i in range(1, steps+1)]
        
        # Create forecast dataframe
        forecast_df = pd.DataFrame({
            'date': forecast_dates,
            'forecast': [forecast_value] * steps
        })
        
        return forecast_df

def train_model(data):
    """Function to train model - for backward compatibility"""
    if data is None:
        return None
        
    forecaster = SalesForecaster()
    
    # Prepare time series data
    processor = forecaster  # Reuse preprocessing methods
    ts_data = processor.create_time_series(data) if hasattr(processor, 'create_time_series') else data
    
    return forecaster