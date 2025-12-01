#!/usr/bin/env python3
"""
Sales Forecast Dashboard Launcher
"""

import subprocess
import sys
import os
import argparse

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False
    except FileNotFoundError:
        print("❌ pip not found. Please ensure Python is properly installed.")
        return False

def run_dashboard(port=8501):
    """Run the Streamlit dashboard"""
    print("🚀 Starting Sales Forecast Dashboard...")
    print(f"📊 Dashboard will be available at: http://localhost:{port}")
    print("⚠️  Press Ctrl+C to stop the dashboard")
    
    # Run Streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            f"--server.port={port}",
            "--server.address=0.0.0.0",
            "--browser.serverAddress=localhost",
            "--theme.base=light"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user.")
    except FileNotFoundError:
        print("❌ Streamlit not found. Please install it with: pip install streamlit")
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")

def run_pipeline():
    """Run the sales forecasting pipeline"""
    print("⚙️  Running Sales Forecasting Pipeline...")
    try:
        # First check if the pipeline module exists
        if not os.path.exists("src/main.py"):
            print("❌ Pipeline module not found at src/main.py")
            print("ℹ️  Please ensure the pipeline files are in the src/ directory")
            return False
            
        from src.main import main
        main()
        return True
    except ImportError as e:
        print(f"❌ Failed to import pipeline: {e}")
        return False
    except Exception as e:
        print(f"❌ Error running pipeline: {e}")
        return False

def create_sample_data():
    """Create sample data if it doesn't exist"""
    print("📊 Creating sample data...")
    
    # Check if data directory exists
    if not os.path.exists("data"):
        os.makedirs("data")
        print("✅ Created data directory")
    
    # Check if sample data exists
    if os.path.exists("data/sample_sales_data.csv"):
        print("✅ Sample data already exists")
        return True
    
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime, timedelta
        
        # Create sample sales data
        np.random.seed(42)
        start_date = datetime(2022, 1, 1)
        end_date = datetime(2023, 12, 31)
        
        # Generate date range
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Generate sample data
        n_records = len(dates) * 15  # ~15 orders per day on average
        
        data = {
            'Order ID': [f'ORD-{i:06d}' for i in range(1, n_records + 1)],
            'Order Date': np.random.choice(dates, n_records),
            'Ship Date': [],
            'Ship Mode': np.random.choice(['Standard', 'Express', 'Next Day'], n_records, p=[0.6, 0.3, 0.1]),
            'Customer ID': [f'CUST-{np.random.randint(1000, 9999)}' for _ in range(n_records)],
            'Customer Name': [f'Customer {i}' for i in range(1, 501) * (n_records // 500)],
            'Segment': np.random.choice(['Consumer', 'Corporate', 'Home Office'], n_records, p=[0.6, 0.3, 0.1]),
            'Country': ['United States'] * n_records,
            'City': np.random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'], n_records),
            'State': np.random.choice(['NY', 'CA', 'IL', 'TX', 'AZ'], n_records),
            'Postal Code': [str(np.random.randint(10000, 99999)) for _ in range(n_records)],
            'Region': np.random.choice(['East', 'West', 'Central', 'South'], n_records),
            'Product ID': [f'PROD-{np.random.randint(1000, 9999)}' for _ in range(n_records)],
            'Category': np.random.choice(['Furniture', 'Office Supplies', 'Technology'], n_records, p=[0.4, 0.4, 0.2]),
            'Sub-Category': np.random.choice(['Chairs', 'Tables', 'Storage', 'Paper', 'Pens', 'Phones', 'Computers'], n_records),
            'Product Name': [f'Product {i}' for i in range(1, 101) * (n_records // 100)],
            'Sales': np.random.exponential(500, n_records).round(2),
            'Quantity': np.random.randint(1, 10, n_records),
            'Discount': np.random.uniform(0, 0.3, n_records).round(2),
            'Profit': []
        }
        
        # Calculate ship dates (1-7 days after order)
        for order_date in data['Order Date']:
            ship_date = order_date + timedelta(days=np.random.randint(1, 8))
            data['Ship Date'].append(ship_date)
        
        # Calculate profit (assuming 20% margin)
        data['Profit'] = (data['Sales'] * np.random.uniform(0.15, 0.25, n_records)).round(2)
        
        df = pd.DataFrame(data)
        
        # Save to CSV
        df.to_csv('data/sample_sales_data.csv', index=False)
        print(f"✅ Created sample data with {len(df)} records")
        print(f"✅ Data saved to: data/sample_sales_data.csv")
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def check_dependencies():
    """Check if all required files exist"""
    print("🔍 Checking dependencies...")
    
    required_files = {
        'app.py': 'Main dashboard application',
        'requirements.txt': 'Python package requirements'
    }
    
    missing_files = []
    
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"✅ {file} - {description}")
        else:
            print(f"❌ {file} - {description} - NOT FOUND")
            missing_files.append(file)
    
    # Check for data
    if not os.path.exists("data/sample_sales_data.csv"):
        print("❌ data/sample_sales_data.csv - Sample data - NOT FOUND")
        missing_files.append("data/sample_sales_data.csv")
    else:
        print("✅ data/sample_sales_data.csv - Sample data")
    
    return missing_files

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Sales Forecasting Dashboard Launcher")
    parser.add_argument(
        "action", 
        nargs="?", 
        default="dashboard",
        choices=["dashboard", "pipeline", "install", "setup", "check"],
        help="Action to perform (dashboard, pipeline, install, setup, check)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8501,
        help="Port to run the dashboard on (default: 8501)"
    )
    parser.add_argument(
        "--create-data",
        action="store_true",
        help="Create sample data if it doesn't exist"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("📊 ADVANCED SALES FORECASTING & BUSINESS INSIGHTS DASHBOARD")
    print("=" * 60)
    
    if args.action == "check":
        missing = check_dependencies()
        if missing:
            print(f"\n⚠️  Missing files: {len(missing)}")
            for file in missing:
                print(f"   - {file}")
            print(f"\n💡 Run './launcher.py setup' to create missing files")
        else:
            print("\n✅ All dependencies are satisfied!")
        return
    
    if args.action == "setup":
        print("\n🛠️  Setting up the dashboard...")
        
        # Create requirements.txt if it doesn't exist
        if not os.path.exists("requirements.txt"):
            print("\n📦 Creating requirements.txt...")
            with open("requirements.txt", "w") as f:
                f.write("""streamlit>=1.28.0
pandas>=2.1.0
numpy>=1.24.0
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0""")
            print("✅ Created requirements.txt")
        
        # Create sample data
        create_sample_data()
        
        # Create basic app.py if it doesn't exist
        if not os.path.exists("app.py"):
            print("\n📝 Creating basic app.py...")
            # We'll create a minimal app.py
            with open("app.py", "w") as f:
                f.write('''import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard")
st.write("Run the full setup to install the complete dashboard.")''')
            print("✅ Created app.py")
        
        print("\n✅ Setup complete!")
        print("\nNext steps:")
        print("1. Run './launcher.py install' to install packages")
        print("2. Run './launcher.py dashboard' to start the dashboard")
        return
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found!")
        response = input("Create requirements.txt? (y/n): ")
        if response.lower() == 'y':
            with open("requirements.txt", "w") as f:
                f.write("""streamlit>=1.28.0
pandas>=2.1.0
numpy>=1.24.0
plotly>=5.17.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0""")
            print("✅ Created requirements.txt")
    
    # Check for sample data
    if args.create_data or not os.path.exists("data/sample_sales_data.csv"):
        if not create_sample_data():
            print("⚠️  Could not create sample data. Dashboard may not work properly.")
    
    if args.action == "install":
        install_requirements()
    elif args.action == "pipeline":
        run_pipeline()
    else:
        # Install requirements first
        success = install_requirements()
        
        if success:
            run_dashboard(args.port)
        else:
            print("⚠️  Continuing without installing requirements...")
            response = input("Do you want to try running the dashboard anyway? (y/n): ")
            if response.lower() == 'y':
                run_dashboard(args.port)

if __name__ == "__main__":
    main()