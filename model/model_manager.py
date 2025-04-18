import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class ModelManager:
    def __init__(self):
        self.data = None
        self.start_date = None
        self.end_date = None
        # Load initial data
        self.fetch_data()  # This will use default dates (last 5 years)

    def fetch_data(self, start_date=None, end_date=None):
        """Fetch S&P 500 data and calculate metrics"""
        try:
            current_date = datetime.now().date()
            
            if start_date is None:
                end_date = current_date
                start_date = end_date - timedelta(days=365*5)
                print("Using default date range")
            else:
                # Convert string dates to datetime.date objects
                if isinstance(start_date, str):
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                # Ensure end_date is not in the future
                if end_date > current_date:
                    end_date = current_date
                    print("Adjusted end date to current date")
                print("Using provided date range")
            
            print(f"Fetching data from {start_date} to {end_date}")
            
            self.start_date = start_date
            self.end_date = end_date
            
            print("Downloading data from Yahoo Finance...")
            sp500 = yf.download('^GSPC', start=start_date, end=end_date)
            print("Download complete")
            
            if sp500.empty:
                print("No data returned from yfinance")
                return pd.DataFrame()
            
            print(f"Successfully fetched {len(sp500)} data points")
            print(f"Data range: from {sp500.index[0]} to {sp500.index[-1]}")
            print(f"Columns available: {sp500.columns.tolist()}")
            
            # Handle MultiIndex columns if present
            if isinstance(sp500.columns, pd.MultiIndex):
                sp500.columns = sp500.columns.get_level_values(0)
            
            # Calculate metrics
            sp500['Daily_Return'] = sp500['Close'].pct_change()
            sp500['Rolling_Std'] = sp500['Daily_Return'].rolling(window=20).std()
            
            self.data = sp500
            return sp500
            
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            print(f"Start date: {start_date}, End date: {end_date}")
            import traceback
            print(f"Full traceback: {traceback.format_exc()}")
            return pd.DataFrame()

    def get_statistics(self):
        """Calculate and return key statistics"""
        if self.data is None or self.data.empty:
            return None
        
        try:
            stats = {
                'current_price': self.data['Close'][-1],
                'total_return': (self.data['Close'][-1] / self.data['Close'][0] - 1) * 100,
                'annual_return': ((1 + (self.data['Close'][-1] / self.data['Close'][0] - 1)) ** (252/len(self.data)) - 1) * 100,
                'annual_volatility': self.data['Daily_Return'].std() * np.sqrt(252) * 100
            }
            
            stats['sharpe_ratio'] = stats['annual_return'] / stats['annual_volatility'] if stats['annual_volatility'] != 0 else 0
            
            return stats
            
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return None

    def get_moving_averages(self):
        """Calculate moving averages"""
        if self.data is None or self.data.empty:
            return None
        
        try:
            return {
                'ma20': self.data['Close'].rolling(window=20).mean(),
                'ma50': self.data['Close'].rolling(window=50).mean()
            }
        except Exception as e:
            print(f"Error calculating moving averages: {e}")
            return None 