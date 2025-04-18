import plotly.graph_objects as go
from dash import html, dcc
import numpy as np

class MonteCarloView:
    @staticmethod
    def create_simulation_plot(simulated_data):
        """Create a plot of Monte Carlo simulation results"""
        if simulated_data is None:
            return html.Div("No simulation data available")
            
        simulated_prices = simulated_data['simulated_prices']
        last_price = simulated_data['last_price']
        stats = simulated_data['statistics']
        
        # Create time array for x-axis
        time_array = np.arange(simulated_prices.shape[0])
        
        # Create figure
        fig = go.Figure()
        
        # Add all simulation paths with low opacity
        for i in range(simulated_prices.shape[1]):
            fig.add_trace(go.Scatter(
                x=time_array,
                y=simulated_prices[:, i],
                mode='lines',
                line=dict(color='rgba(0, 0, 255, 0.1)'),
                showlegend=False
            ))
            
        # Add mean path
        mean_path = np.mean(simulated_prices, axis=1)
        fig.add_trace(go.Scatter(
            x=time_array,
            y=mean_path,
            mode='lines',
            line=dict(color='red', width=2),
            name='Mean Path'
        ))
        
        # Add 95% confidence interval
        percentile_95 = np.percentile(simulated_prices, 95, axis=1)
        percentile_5 = np.percentile(simulated_prices, 5, axis=1)
        
        fig.add_trace(go.Scatter(
            x=time_array,
            y=percentile_95,
            mode='lines',
            line=dict(color='rgba(0, 255, 0, 0.5)'),
            name='95th Percentile'
        ))
        
        fig.add_trace(go.Scatter(
            x=time_array,
            y=percentile_5,
            mode='lines',
            line=dict(color='rgba(0, 255, 0, 0.5)'),
            name='5th Percentile',
            fill='tonexty'
        ))
        
        # Update layout
        fig.update_layout(
            title='Monte Carlo Simulation of S&P 500',
            xaxis_title='Trading Days',
            yaxis_title='Price',
            showlegend=True,
            template='plotly_white'
        )
        
        return dcc.Graph(figure=fig)
    
    @staticmethod
    def create_statistics_table(stats):
        """Create a table displaying simulation statistics"""
        if stats is None:
            return html.Div("No statistics available")
            
        return html.Div([
            html.H3("Simulation Statistics"),
            html.Table([
                html.Tr([html.Th("Metric"), html.Th("Value")]),
                html.Tr([html.Td("Mean Price"), html.Td(f"${stats['mean']:.2f}")]),
                html.Tr([html.Td("Median Price"), html.Td(f"${stats['median']:.2f}")]),
                html.Tr([html.Td("Standard Deviation"), html.Td(f"${stats['std']:.2f}")]),
                html.Tr([html.Td("Minimum Price"), html.Td(f"${stats['min']:.2f}")]),
                html.Tr([html.Td("Maximum Price"), html.Td(f"${stats['max']:.2f}")]),
                html.Tr([html.Td("95th Percentile"), html.Td(f"${stats['percentile_95']:.2f}")]),
                html.Tr([html.Td("5th Percentile"), html.Td(f"${stats['percentile_5']:.2f}")])
            ], style={'width': '100%', 'border': '1px solid black'})
        ])
        
    @staticmethod
    def create_insights_panel(simulated_data):
        """Create a panel with practical insights from the simulation"""
        if simulated_data is None:
            return html.Div("No simulation data available for insights")
            
        simulated_prices = simulated_data['simulated_prices']
        last_price = simulated_data['last_price']
        stats = simulated_data['statistics']
        
        # Calculate additional metrics
        final_prices = simulated_prices[-1]
        price_increase_prob = np.mean(final_prices > last_price) * 100
        price_decrease_prob = np.mean(final_prices < last_price) * 100
        price_double_prob = np.mean(final_prices > last_price * 2) * 100
        price_halve_prob = np.mean(final_prices < last_price * 0.5) * 100
        
        # Calculate expected return
        expected_return = ((stats['mean'] / last_price) - 1) * 100
        
        # Calculate risk metrics
        downside_risk = ((last_price - stats['percentile_5']) / last_price) * 100
        upside_potential = ((stats['percentile_95'] - last_price) / last_price) * 100
        
        return html.Div([
            html.H3("Practical Insights", style={'textAlign': 'center', 'marginTop': 20}),
            
            html.Div([
                html.H4("Probability Analysis", style={'color': '#2c3e50'}),
                html.P([
                    html.Strong(f"Probability of price increase: "), 
                    f"{price_increase_prob:.1f}%"
                ]),
                html.P([
                    html.Strong(f"Probability of price decrease: "), 
                    f"{price_decrease_prob:.1f}%"
                ]),
                html.P([
                    html.Strong(f"Probability of price doubling: "), 
                    f"{price_double_prob:.1f}%"
                ]),
                html.P([
                    html.Strong(f"Probability of price halving: "), 
                    f"{price_halve_prob:.1f}%"
                ])
            ], style={'marginBottom': 20}),
            
            html.Div([
                html.H4("Risk-Return Profile", style={'color': '#2c3e50'}),
                html.P([
                    html.Strong(f"Expected return: "), 
                    f"{expected_return:.1f}%"
                ]),
                html.P([
                    html.Strong(f"Downside risk: "), 
                    f"{downside_risk:.1f}%"
                ]),
                html.P([
                    html.Strong(f"Upside potential: "), 
                    f"{upside_potential:.1f}%"
                ])
            ], style={'marginBottom': 20}),
            
            html.Div([
                html.H4("Key Conclusions", style={'color': '#2c3e50'}),
                html.Ul([
                    html.Li("The simulation provides a range of possible future prices based on historical volatility and returns."),
                    html.Li(f"The median projected price is ${stats['median']:.2f}, which represents the most likely outcome."),
                    html.Li(f"There is a 90% probability that the price will fall between ${stats['percentile_5']:.2f} and ${stats['percentile_95']:.2f}."),
                    html.Li(f"The expected return of {expected_return:.1f}% represents the average outcome across all simulations."),
                    html.Li("This simulation assumes that future price movements will follow the same statistical properties as historical data.")
                ])
            ])
        ], style={'padding': 20, 'backgroundColor': '#f8f9fa', 'borderRadius': 5, 'marginTop': 20}) 