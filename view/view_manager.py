from dash import html, dcc
import plotly.graph_objects as go
from datetime import datetime, timedelta
from .monte_carlo_view import MonteCarloView

class ViewManager:
    def __init__(self):
        self.layout = None
        self.monte_carlo_view = MonteCarloView()

    def create_layout(self):
        """Create the main layout of the dashboard"""
        self.layout = html.Div([
            html.H1('S&P 500 Analysis Dashboard', 
                    style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
            
            # Date range selector
            self._create_date_selector(),
            
            # Loading state with all charts
            dcc.Loading(
                id="loading",
                type="default",
                children=[
                    self._create_price_chart(),
                    self._create_secondary_charts(),
                    self._create_stats_panel(),
                    self._create_monte_carlo_section()
                ]
            )
        ])
        return self.layout

    def _create_date_selector(self):
        """Create the date range selector component"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)  # Remove .date() since we're already working with date objects
        
        return html.Div([
            html.Label('Select Date Range:', style={'marginRight': 10}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=start_date,
                end_date=end_date,
                max_date_allowed=end_date,
                min_date_allowed=datetime(2000, 1, 1).date(),
                initial_visible_month=end_date,
                style={'marginBottom': 20}
            ),
            html.Button('Update Charts', id='update-button', n_clicks=0,
                       style={'marginLeft': 10, 'padding': '5px 10px'})
        ], style={'marginBottom': 20, 'display': 'flex', 'alignItems': 'center'})

    def _create_price_chart(self):
        """Create the main price chart container"""
        return html.Div([
            dcc.Graph(id='price-chart', style={'height': '600px'})
        ], style={'marginBottom': 30})

    def _create_secondary_charts(self):
        """Create the returns and volatility charts container"""
        return html.Div([
            html.Div([
                dcc.Graph(id='returns-chart')
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(id='volatility-chart')
            ], style={'width': '50%', 'display': 'inline-block'})
        ])

    def _create_stats_panel(self):
        """Create the statistics panel"""
        return html.Div([
            html.H3('Key Statistics', style={'textAlign': 'center'}),
            html.Div(id='stats-panel', style={'textAlign': 'center'})
        ], style={'marginTop': 20, 'padding': 20, 'backgroundColor': '#f8f9fa', 'borderRadius': 5})

    def _create_monte_carlo_section(self):
        """Create the Monte Carlo simulation section"""
        return html.Div([
            html.H2('Monte Carlo Simulation', 
                    style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': 30, 'marginBottom': 20}),
            
            # Simulation controls
            html.Div([
                html.Label('Number of Days:', style={'marginRight': 10}),
                dcc.Input(
                    id='simulation-days',
                    type='number',
                    value=252,
                    min=1,
                    max=1000,
                    style={'width': 100, 'marginRight': 20}
                ),
                
                html.Label('Number of Simulations:', style={'marginRight': 10}),
                dcc.Input(
                    id='simulation-count',
                    type='number',
                    value=1000,
                    min=100,
                    max=10000,
                    style={'width': 100, 'marginRight': 20}
                ),
                
                html.Button('Run Simulation', id='run-simulation-button', n_clicks=0,
                           style={'padding': '5px 10px'})
            ], style={'marginBottom': 20, 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            
            # Simulation results
            html.Div([
                html.Div(id='monte-carlo-plot', style={'width': '70%', 'display': 'inline-block'}),
                html.Div(id='monte-carlo-stats', style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
            ], style={'marginTop': 20}),
            
            # Insights panel
            html.Div(id='monte-carlo-insights', style={'marginTop': 20})
        ], style={'marginTop': 30, 'padding': 20, 'backgroundColor': '#f8f9fa', 'borderRadius': 5})

    def create_price_figure(self, data, moving_averages):
        """Create the price chart figure"""
        if data is None or data.empty:
            return go.Figure()
        
        # Create candlestick chart
        fig = go.Figure(data=[go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='S&P 500',
            increasing_line_color='#26a69a',  # Green for increasing
            decreasing_line_color='#ef5350',  # Red for decreasing
            showlegend=True
        )])
        
        # Add moving averages with improved visibility
        if moving_averages:
            fig.add_trace(go.Scatter(
                x=data.index,
                y=moving_averages['ma20'],
                name='20-day MA',
                line=dict(color='#2196F3', width=1.5, dash='dot'),
                opacity=0.7
            ))
            
            fig.add_trace(go.Scatter(
                x=data.index,
                y=moving_averages['ma50'],
                name='50-day MA',
                line=dict(color='#FF5722', width=1.5, dash='dot'),
                opacity=0.7
            ))
        
        # Update layout with improved formatting
        fig.update_layout(
            title={
                'text': 'S&P 500 Price History',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=20)
            },
            xaxis_title='Date',
            yaxis_title='Price (USD)',
            template='plotly_white',
            xaxis_rangeslider_visible=False,  # Disable rangeslider for cleaner look
            height=600,
            yaxis=dict(
                title=dict(
                    text='Price (USD)',
                    font=dict(size=14)
                ),
                tickfont=dict(size=12),
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True
            ),
            xaxis=dict(
                title=dict(
                    text='Date',
                    font=dict(size=14)
                ),
                tickfont=dict(size=12),
                gridcolor='rgba(0,0,0,0.1)',
                showgrid=True,
                rangeslider=dict(visible=False)
            ),
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.99,
                xanchor="left",
                x=0.01,
                bgcolor='rgba(255, 255, 255, 0.8)',
                bordercolor='rgba(0,0,0,0.2)',
                borderwidth=1
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(t=80, b=40, l=40, r=40)
        )
        
        # Add buttons for time range selection
        data_length = len(data)
        last_date = data.index[-1]
        
        # Calculate dynamic ranges based on available data
        ranges = {
            "1M": min(30, data_length),
            "6M": min(180, data_length),
            "1Y": min(365, data_length),
            "5Y": min(1825, data_length)
        }
        
        fig.update_layout(
            updatemenus=[
                dict(
                    buttons=list([
                        dict(
                            args=[{'xaxis.range': [data.index[-ranges["1M"]], last_date]}],
                            label="1M",
                            method="relayout"
                        ),
                        dict(
                            args=[{'xaxis.range': [data.index[-ranges["6M"]], last_date]}],
                            label="6M",
                            method="relayout"
                        ),
                        dict(
                            args=[{'xaxis.range': [data.index[data.index.year == last_date.year][0], last_date]}],
                            label="YTD",
                            method="relayout"
                        ),
                        dict(
                            args=[{'xaxis.range': [data.index[-ranges["1Y"]], last_date]}],
                            label="1Y",
                            method="relayout"
                        ),
                        dict(
                            args=[{'xaxis.range': [data.index[-ranges["5Y"]], last_date]}],
                            label="5Y",
                            method="relayout"
                        ),
                        dict(
                            args=[{'xaxis.range': [data.index[0], last_date]}],
                            label="MAX",
                            method="relayout"
                        )
                    ]),
                    direction="down",
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.1,
                    xanchor="left",
                    y=1.1,
                    yanchor="top"
                )
            ]
        )
        
        return fig

    def create_returns_figure(self, data):
        """Create the returns chart figure"""
        if data is None or data.empty:
            return go.Figure()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Daily_Return'] * 100,
            name='Daily Returns',
            line=dict(color='#3498db')
        ))
        
        fig.update_layout(
            title='Daily Returns (%)',
            xaxis_title='Date',
            yaxis_title='Return (%)',
            template='plotly_white',
            height=400
        )
        
        return fig

    def create_volatility_figure(self, data):
        """Create the volatility chart figure"""
        if data is None or data.empty:
            return go.Figure()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=data.index,
            y=data['Rolling_Std'] * 100,
            name='20-day Rolling Volatility',
            line=dict(color='#e74c3c')
        ))
        
        fig.update_layout(
            title='20-day Rolling Volatility (%)',
            xaxis_title='Date',
            yaxis_title='Volatility (%)',
            template='plotly_white',
            height=400
        )
        
        return fig

    def create_stats_panel(self, stats):
        """Create the statistics panel content"""
        if stats is None:
            return html.Div("No data available for the selected date range")
        
        return html.Div([
            html.P(f'Current Price: ${stats["current_price"]:.2f}', 
                  style={'margin': '5px', 'fontWeight': 'bold'}),
            html.P(f'Total Return: {stats["total_return"]:.2f}%', 
                  style={'margin': '5px'}),
            html.P(f'Annual Return: {stats["annual_return"]:.2f}%', 
                  style={'margin': '5px'}),
            html.P(f'Annual Volatility: {stats["annual_volatility"]:.2f}%', 
                  style={'margin': '5px'}),
            html.P(f'Sharpe Ratio: {stats["sharpe_ratio"]:.2f}', 
                  style={'margin': '5px'})
        ]) 