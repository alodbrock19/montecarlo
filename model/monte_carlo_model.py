import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

class MonteCarloSimulation:
    def __init__(self, symbol='^GSPC', days=252, simulations=1000):
        """
        Initialize Monte Carlo simulation for S&P 500
        
        Parameters:
        -----------
        symbol : str
            Stock symbol (default: ^GSPC for S&P 500)
        days : int
            Number of trading days to simulate
        simulations : int
            Number of Monte Carlo simulations to run
        """
        self.symbol = symbol
        self.days = days
        self.simulations = simulations
        self.data = None
        self.mean_return = None
        self.volatility = None
        
    def fetch_data(self):
        """Fetch historical data for the symbol"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            self.data = yf.download(self.symbol, start=start_date, end=end_date)
            
            if self.data.empty:
                print(f"No data available for {self.symbol}")
                return None
            
            # Handle MultiIndex columns if present
            if isinstance(self.data.columns, pd.MultiIndex):
                self.data.columns = self.data.columns.get_level_values(0)
                
            return self.data
        except Exception as e:
            print(f"Error fetching data: {str(e)}")
            return None
    
    def calculate_parameters(self):
        """Calculate mean return and volatility from historical data"""
        try:
            if self.data is None:
                self.data = self.fetch_data()
                if self.data is None:
                    return None, None
                
            # Calculate daily returns using Close price
            returns = np.log(1 + self.data['Close'].pct_change())
            
            # Remove any NaN values
            returns = returns.dropna()
            
            if len(returns) == 0:
                print("No valid returns data available")
                return None, None
            
            # Calculate mean return and volatility
            self.mean_return = returns.mean()
            self.volatility = returns.std()
            
            return self.mean_return, self.volatility
        except Exception as e:
            print(f"Error calculating parameters: {str(e)}")
            return None, None
    
    def simulate(self):
        """Run Monte Carlo simulation"""
        try:
            if self.mean_return is None or self.volatility is None:
                mean_return, volatility = self.calculate_parameters()
                if mean_return is None or volatility is None:
                    return None
                
            if self.data is None or self.data.empty:
                print("No historical data available for simulation")
                return None
                
            # Get the last price
            last_price = self.data['Close'].iloc[-1]
            
            # Create price array
            price_array = np.zeros((self.days, self.simulations))
            price_array[0] = last_price
            
            # Generate price paths
            for t in range(1, self.days):
                # Generate random returns
                returns = np.random.normal(
                    loc=self.mean_return,
                    scale=self.volatility,
                    size=self.simulations
                )
                
                # Calculate price
                price_array[t] = price_array[t-1] * np.exp(returns)
                
            return price_array
        except Exception as e:
            print(f"Error running simulation: {str(e)}")
            return None
    
    def get_statistics(self, simulated_prices):
        """Calculate statistics from simulated prices"""
        try:
            if simulated_prices is None:
                return None
                
            final_prices = simulated_prices[-1]
            
            stats = {
                'mean': np.mean(final_prices),
                'median': np.median(final_prices),
                'std': np.std(final_prices),
                'min': np.min(final_prices),
                'max': np.max(final_prices),
                'percentile_95': np.percentile(final_prices, 95),
                'percentile_5': np.percentile(final_prices, 5)
            }
            
            return stats
        except Exception as e:
            print(f"Error calculating statistics: {str(e)}")
            return None 