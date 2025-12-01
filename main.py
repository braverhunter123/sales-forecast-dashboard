#!/usr/bin/env python3
"""
Sales Forecasting & Business Insights Dashboard
Main Application Entry Point
"""

import sys
import os
import argparse
from src.main import main as pipeline_main

def show_help():
    """Display help information"""
    print("""
Sales Forecasting & Business Insights Dashboard
==============================================

Usage:
    python main.py [command] [options]

Commands:
    run         Run the complete sales forecasting pipeline
    dashboard   Start the Streamlit dashboard
    help        Show this help message

Examples:
    python main.py run
    python main.py dashboard
    python main.py help

For more information, check the README.md file.
    """)

def run_dashboard():
    """Run the Streamlit dashboard"""
    try:
        import subprocess
        import sys
        
        print("🚀 Starting Sales Forecast Dashboard...")
        print("📊 Dashboard will be available at: http://localhost:8501")
        print("⚠️  Press Ctrl+C to stop the dashboard")
        
        # Run Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py", 
                       "--server.port=8501", "--server.address=0.0.0.0"])
    except Exception as e:
        print(f"❌ Error running dashboard: {e}")
        print("Please make sure Streamlit is installed: pip install streamlit")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Sales Forecasting & Business Insights Dashboard")
    parser.add_argument('command', nargs='?', default='help', 
                       choices=['run', 'dashboard', 'help'],
                       help='Command to execute')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        print("🚀 Starting Sales Forecasting Pipeline...")
        pipeline_main()
    elif args.command == 'dashboard':
        run_dashboard()
    else:
        show_help()

if __name__ == "__main__":
    main()