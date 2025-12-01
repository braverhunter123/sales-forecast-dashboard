"""
Visualization utilities for the dashboard
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class Visualizations:
    def __init__(self):
        self.color_palette = px.colors.qualitative.Set3
        # Set default template
        px.defaults.template = "plotly_white"
    
    def create_sales_trend(self, df, date_col='date', value_col='sales'):
        """Create sales trend chart with moving averages"""
        fig = go.Figure()
        
        # Actual sales line
        fig.add_trace(go.Scatter(
            x=df[date_col],
            y=df[value_col],
            mode='lines',
            name='Actual Sales',
            line=dict(color='#2980b9', width=2)
        ))
        
        # 7-day moving average
        if '7_day_MA' in df.columns:
            fig.add_trace(go.Scatter(
                x=df[date_col],
                y=df['7_day_MA'],
                mode='lines',
                name='7-Day Moving Average',
                line=dict(color='#e74c3c', width=2, dash='dash')
            ))
        
        # 30-day moving average
        if '30_day_MA' in df.columns:
            fig.add_trace(go.Scatter(
                x=df[date_col],
                y=df['30_day_MA'],
                mode='lines',
                name='30-Day Moving Average',
                line=dict(color='#27ae60', width=2, dash='dot')
            ))
        
        fig.update_layout(
            title="Sales Trend Analysis with Moving Averages",
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            hovermode='x unified',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_forecast_plot(self, history_df, forecast_df, actual_df=None):
        """Create forecast visualization"""
        fig = go.Figure()
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=history_df['date'],
            y=history_df['sales'],
            name='Historical',
            line=dict(color='#2980b9', width=2),
            mode='lines+markers'
        ))
        
        # Forecast
        fig.add_trace(go.Scatter(
            x=forecast_df['date'],
            y=forecast_df['forecast'],
            name='Forecast',
            line=dict(color='#e74c3c', width=2, dash='dash'),
            mode='lines+markers'
        ))
        
        # Confidence interval (if available)
        if 'lower_bound' in forecast_df.columns and 'upper_bound' in forecast_df.columns:
            fig.add_trace(go.Scatter(
                x=pd.concat([forecast_df['date'], forecast_df['date'][::-1]]),
                y=pd.concat([forecast_df['upper_bound'], forecast_df['lower_bound'][::-1]]),
                fill='toself',
                fillcolor='rgba(231, 76, 60, 0.2)',
                line=dict(color='rgba(255,255,255,0)'),
                hoverinfo="skip",
                showlegend=True,
                name='Confidence Interval'
            ))
        
        # Actual (if provided)
        if actual_df is not None:
            fig.add_trace(go.Scatter(
                x=actual_df['date'],
                y=actual_df['sales'],
                name='Actual',
                line=dict(color='#27ae60', width=2),
                mode='lines+markers'
            ))
        
        fig.update_layout(
            title="Sales Forecast Visualization",
            xaxis_title="Date",
            yaxis_title="Sales ($)",
            hovermode='x unified',
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_category_analysis(self, df, category_col='Category', value_col='Sales'):
        """Create category-wise sales analysis"""
        category_sales = df.groupby(category_col)[value_col].sum().reset_index()
        category_sales = category_sales.sort_values(value_col, ascending=False)
        
        fig = px.bar(
            category_sales,
            x=category_col,
            y=value_col,
            title=f"Sales by {category_col}",
            color=value_col,
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(
            xaxis_title=category_col,
            yaxis_title="Total Sales ($)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_geographic_analysis(self, df, location_col='State', value_col='Sales'):
        """Create geographic sales distribution"""
        geo_sales = df.groupby(location_col)[value_col].sum().reset_index()
        geo_sales = geo_sales.sort_values(value_col, ascending=False).head(15)
        
        fig = px.bar(
            geo_sales,
            x=location_col,
            y=value_col,
            title=f"Top 15 {location_col} by Sales",
            color=value_col,
            color_continuous_scale='Teal'
        )
        
        fig.update_layout(
            xaxis_title=location_col,
            yaxis_title="Total Sales ($)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_customer_segmentation(self, df, segment_col='Segment', value_col='Sales'):
        """Create customer segmentation analysis"""
        segment_data = df.groupby(segment_col)[value_col].agg(['sum', 'count']).reset_index()
        segment_data.columns = [segment_col, 'Total_Sales', 'Order_Count']
        
        # Create subplot with two charts
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Sales by Segment', 'Order Count by Segment'),
            specs=[[{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Pie chart for sales distribution
        fig.add_trace(
            go.Pie(
                labels=segment_data[segment_col],
                values=segment_data['Total_Sales'],
                name="Sales",
                marker_colors=["#a0a9af", '#2ecc71', '#e74c3c', '#f39c12']
            ),
            row=1, col=1
        )
        
        # Bar chart for order count
        fig.add_trace(
            go.Bar(
                x=segment_data[segment_col],
                y=segment_data['Order_Count'],
                name="Order Count",
                marker_color="#b172ca"
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title_text="Customer Segmentation Analysis",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    def create_product_performance(self, df, product_col='Product Name', value_col='Sales'):
        """Create top performing products analysis"""
        top_products = df.groupby(product_col)[value_col].sum().reset_index()
        top_products = top_products.sort_values(value_col, ascending=False).head(10)
        
        fig = px.bar(
            top_products,
            x=value_col,
            y=product_col,
            orientation='h',
            title="Top 10 Products by Sales",
            color=value_col,
            color_continuous_scale='Purp'
        )
        
        fig.update_layout(
            xaxis_title="Total Sales ($)",
            yaxis_title="Product Name",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig

def plot_forecast_results(model):
    """Function to plot forecast results - for backward compatibility"""
    print("Plotting forecast results...")
    # Placeholder for actual plotting implementation
    pass