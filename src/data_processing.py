"""
Data processing utilities for the sales forecasting dashboard
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self):
        pass
    
    def load_and_preprocess(self, file_path="data/sample_sales_data.csv"):
        """Load and preprocess sales data"""
        try:
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print(f"Error: Could not find {file_path}")
            return None
        except Exception as e:
            print(f"Error loading data: {e}")
            return None
            
        # Convert date columns
        date_columns = ['Order Date', 'Ship Date']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format='%d/%m/%Y')
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        
        # Handle categorical missing values
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            df[col] = df[col].fillna('Unknown')
        
        # Create additional features from Order Date
        if 'Order Date' in df.columns:
            df['date'] = df['Order Date']  # Create a standard date column
            df['year'] = df['Order Date'].dt.year
            df['month'] = df['Order Date'].dt.month
            df['day'] = df['Order Date'].dt.day
            df['day_of_week'] = df['Order Date'].dt.dayofweek
            df['quarter'] = df['Order Date'].dt.quarter
            df['week_of_year'] = df['Order Date'].dt.isocalendar().week
            df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)  # Saturday and Sunday
            
        # Create additional business metrics
        if 'Sales' in df.columns:
            df['Profit'] = df['Sales'] * 0.2  # Assuming 20% profit margin
            df['Sales_per_order'] = df.groupby('Order ID')['Sales'].transform('sum')
            
        if 'Order Date' in df.columns and 'Ship Date' in df.columns:
            df['Order Processing Time'] = (df['Ship Date'] - df['Order Date']).dt.days
            
        # Create customer metrics
        if 'Customer ID' in df.columns:
            df['Customer Order Count'] = df.groupby('Customer ID')['Order ID'].transform('nunique')
            df['Customer Total Sales'] = df.groupby('Customer ID')['Sales'].transform('sum')
            
        return df
    
    def create_time_series(self, df, date_col='Order Date', value_col='Sales'):
        """Create time series data"""
        if date_col not in df.columns or value_col not in df.columns:
            # Try alternative column names
            if 'Order Date' in df.columns and 'Sales' in df.columns:
                date_col, value_col = 'Order Date', 'Sales'
            else:
                raise ValueError(f"Required columns '{date_col}' and '{value_col}' not found")
        
        # Group by date and sum the values
        ts_df = df.groupby(date_col)[value_col].sum().reset_index()
        ts_df = ts_df.rename(columns={date_col: 'date', value_col: 'sales'})
        ts_df = ts_df.sort_values('date').reset_index(drop=True)
        
        # Add additional time-based features
        ts_df['year'] = ts_df['date'].dt.year
        ts_df['month'] = ts_df['date'].dt.month
        ts_df['day'] = ts_df['date'].dt.day
        ts_df['day_of_week'] = ts_df['date'].dt.dayofweek
        ts_df['quarter'] = ts_df['date'].dt.quarter
        ts_df['week_of_year'] = ts_df['date'].dt.isocalendar().week
        
        # Calculate moving averages
        ts_df['7_day_MA'] = ts_df['sales'].rolling(window=7).mean()
        ts_df['30_day_MA'] = ts_df['sales'].rolling(window=30).mean()
        
        return ts_df
    
    def prepare_features(self, df, target_col='sales'):
        """Prepare features for ML models"""
        features = df.copy()
        
        # Add time-based features
        if 'date' in features.columns:
            features['year'] = features['date'].dt.year
            features['month'] = features['date'].dt.month
            features['day'] = features['date'].dt.day
            features['day_of_week'] = features['date'].dt.dayofweek
            features['quarter'] = features['date'].dt.quarter
            features['week_of_year'] = features['date'].dt.isocalendar().week
            features['is_weekend'] = features['day_of_week'].isin([5, 6]).astype(int)
            
        # Remove non-numeric columns except date
        numeric_features = features.select_dtypes(include=[np.number]).columns.tolist()
        if 'date' in features.columns:
            feature_cols = ['date'] + numeric_features
            features = features[feature_cols]
            
        return features
    
    def detect_outliers(self, df, column='Sales', threshold=3):
        """Detect outliers using Z-score method"""
        z_scores = np.abs((df[column] - df[column].mean()) / df[column].std())
        outliers = df[z_scores > threshold]
        return outliers
    
    def segment_customers(self, df, sales_col='Sales'):
        """Segment customers based on purchasing behavior"""
        if 'Customer ID' not in df.columns:
            raise ValueError("Customer ID column not found")
            
        customer_stats = df.groupby('Customer ID')[sales_col].agg(['sum', 'count', 'mean']).reset_index()
        customer_stats.columns = ['Customer ID', 'Total_Sales', 'Order_Count', 'Avg_Order_Value']
        
        # Define segmentation rules
        high_value = customer_stats['Total_Sales'].quantile(0.8)
        frequent = customer_stats['Order_Count'].quantile(0.8)
        
        def categorize_customer(row):
            if row['Total_Sales'] >= high_value and row['Order_Count'] >= frequent:
                return 'VIP'
            elif row['Total_Sales'] >= high_value:
                return 'High Value'
            elif row['Order_Count'] >= frequent:
                return 'Frequent'
            else:
                return 'Regular'
        
        customer_stats['Segment'] = customer_stats.apply(categorize_customer, axis=1)
        return customer_stats

def load_and_clean_data():
    """Function to load and clean data - for backward compatibility"""
    processor = DataProcessor()
    return processor.load_and_preprocess()