"""
Main module to orchestrate the sales forecasting pipeline
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

from .data_processing import DataProcessor
from .modeling import SalesForecaster
from .visualization import Visualizations

def main():
    """Main function to orchestrate the sales forecasting pipeline."""
    print("🚀 Starting Sales Forecasting Pipeline...")
    
    # Initialize components
    processor = DataProcessor()
    forecaster = SalesForecaster()
    viz = Visualizations()
    
    # Data processing step
    print("📂 Loading and preprocessing data...")
    raw_data = processor.load_and_preprocess()
    
    if raw_data is None:
        print("❌ Failed to load data. Exiting.")
        return
    
    # Create time series data
    print("📈 Creating time series data...")
    ts_data = processor.create_time_series(raw_data)
    
    # Display basic info
    print(f"✅ Loaded {len(raw_data)} records")
    print(f"📅 Time series data covers {ts_data['date'].min()} to {ts_data['date'].max()}")
    print(f"💰 Total sales: ${ts_data['sales'].sum():,.2f}")
    
    # Prepare data for training
    print("🤖 Preparing data for model training...")
    try:
        X_train, X_test, y_train, y_test = forecaster.prepare_data_for_training(ts_data)
        print("✅ Data preparation completed")
    except Exception as e:
        print(f"❌ Error in data preparation: {e}")
        return
    
    # Model training step
    print("🧠 Training forecasting model...")
    try:
        forecaster.train(X_train, y_train)
        print("✅ Model training completed")
    except Exception as e:
        print(f"❌ Error in model training: {e}")
        return
    
    # Model evaluation
    print("📊 Evaluating model performance...")
    try:
        metrics = forecaster.evaluate(X_test, y_test)
        print(f"✅ Model Evaluation:")
        print(f"   MAE: ${metrics['mae']:,.2f}")
        print(f"   RMSE: ${metrics['rmse']:,.2f}")
    except Exception as e:
        print(f"❌ Error in model evaluation: {e}")
        return
    
    # Generate sample forecast for next 30 days
    print("🔮 Generating sample forecast...")
    try:
        # Create future dates for forecasting
        last_date = ts_data['date'].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, 31)]
        
        # For demo purposes, we'll generate random forecast values
        # In a real implementation, we would use the trained model to predict
        forecast_values = np.random.normal(y_train.mean(), y_train.std(), 30)
        forecast_values = np.maximum(forecast_values, 0)  # Ensure non-negative values
        
        forecast_df = pd.DataFrame({
            'date': future_dates,
            'forecast': forecast_values
        })
        
        print("✅ Sample forecast generated")
    except Exception as e:
        print(f"❌ Error in forecast generation: {e}")
        return
    
    # Visualization step
    print("🎨 Generating visualizations...")
    try:
        # Create sales trend visualization
        trend_fig = viz.create_sales_trend(ts_data)
        
        # Create forecast visualization
        forecast_fig = viz.create_forecast_plot(ts_data.tail(100), forecast_df)
        
        # Create category analysis
        category_fig = viz.create_category_analysis(raw_data)
        
        print("✅ Visualizations generated")
    except Exception as e:
        print(f"❌ Error in visualization generation: {e}")
        return
    
    print("🎉 Pipeline completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Run the Streamlit dashboard: streamlit run app.py")
    print("   2. Access the dashboard at http://localhost:8501")
    print("   3. Explore the interactive visualizations and filters")

if __name__ == "__main__":
    main()