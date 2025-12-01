"""
Unit tests for data processing module
"""

import unittest
import pandas as pd
import numpy as np
from src.data_processing import DataProcessor

class TestDataProcessor(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.processor = DataProcessor()
        self.sample_data = pd.DataFrame({
            'Order Date': ['01/01/2020', '02/01/2020', '03/01/2020'],
            'Ship Date': ['02/01/2020', '03/01/2020', '04/01/2020'],
            'Sales': [100, 200, 150],
            'Category': ['Furniture', 'Office Supplies', 'Technology']
        })
    
    def test_load_and_preprocess(self):
        """Test data loading and preprocessing"""
        # This test would normally load from a file
        # For demo purposes, we'll test the preprocessing logic
        processed = self.processor.load_and_preprocess("data/sample_sales_data.csv")
        self.assertIsNotNone(processed)
        
    def test_create_time_series(self):
        """Test time series creation"""
        # Create a simple test case
        df = pd.DataFrame({
            'Order Date': pd.to_datetime(['01/01/2020', '01/01/2020', '02/01/2020'], format='%d/%m/%Y'),
            'Sales': [100, 200, 150]
        })
        
        ts_data = self.processor.create_time_series(df)
        self.assertEqual(len(ts_data), 2)  # Two unique dates
        self.assertIn('date', ts_data.columns)
        self.assertIn('sales', ts_data.columns)
        
    def test_prepare_features(self):
        """Test feature preparation"""
        df = pd.DataFrame({
            'Order Date': pd.to_datetime(['01/01/2020', '02/01/2020'], format='%d/%m/%Y'),
            'Sales': [100, 200]
        })
        
        features = self.processor.prepare_features(df)
        self.assertIn('year', features.columns)
        self.assertIn('month', features.columns)
        self.assertIn('day', features.columns)

if __name__ == '__main__':
    unittest.main()