from dash.dependencies import Input, Output, State
from datetime import datetime
from dash import html

class ControllerManager:
    def __init__(self, app, model_manager, view_manager):
        self.app = app
        self.model = model_manager
        self.view = view_manager
        self.setup_callbacks()

    def setup_callbacks(self):
        """Setup all callbacks for the dashboard"""
        @self.app.callback(
            Output('price-chart', 'figure'),
            [Input('update-button', 'n_clicks')],
            [State('date-range', 'start_date'),
             State('date-range', 'end_date')]
        )
        def update_price_chart(n_clicks, start_date, end_date):
            print(f"Updating price chart. Clicks: {n_clicks}, Start: {start_date}, End: {end_date}")
            data = self.model.fetch_data(start_date, end_date)
            moving_averages = self.model.get_moving_averages()
            return self.view.create_price_figure(data, moving_averages)

        @self.app.callback(
            Output('returns-chart', 'figure'),
            [Input('update-button', 'n_clicks')],
            [State('date-range', 'start_date'),
             State('date-range', 'end_date')]
        )
        def update_returns_chart(n_clicks, start_date, end_date):
            print(f"Updating returns chart. Clicks: {n_clicks}, Start: {start_date}, End: {end_date}")
            data = self.model.fetch_data(start_date, end_date)
            return self.view.create_returns_figure(data)

        @self.app.callback(
            Output('volatility-chart', 'figure'),
            [Input('update-button', 'n_clicks')],
            [State('date-range', 'start_date'),
             State('date-range', 'end_date')]
        )
        def update_volatility_chart(n_clicks, start_date, end_date):
            data = self.model.fetch_data(start_date, end_date)
            return self.view.create_volatility_figure(data)

        @self.app.callback(
            Output('stats-panel', 'children'),
            [Input('update-button', 'n_clicks')],
            [State('date-range', 'start_date'),
             State('date-range', 'end_date')]
        )
        def update_stats(n_clicks, start_date, end_date):
            self.model.fetch_data(start_date, end_date)
            stats = self.model.get_statistics()
            return self.view.create_stats_panel(stats)

        @self.app.callback(
            [Output('monte-carlo-plot', 'children'),
             Output('monte-carlo-stats', 'children')],
            [Input('run-simulation-button', 'n_clicks')],
            [State('simulation-days', 'value'),
             State('simulation-count', 'value')]
        )
        def update_monte_carlo_simulation(n_clicks, days, simulations):
            if n_clicks is None or n_clicks == 0:
                return self.view.monte_carlo_view.create_simulation_plot(None), \
                       self.view.monte_carlo_view.create_statistics_table(None)
            
            # Run simulation
            simulated_data = self.model.run_monte_carlo_simulation(days, simulations)
            
            # Handle case when simulation fails
            if simulated_data is None:
                return html.Div("Error: Simulation failed to run. Please check the console for details."), \
                       html.Div("No statistics available")
            
            # Create visualization components
            plot = self.view.monte_carlo_view.create_simulation_plot(simulated_data)
            stats = self.view.monte_carlo_view.create_statistics_table(simulated_data['statistics'])
            
            return plot, stats 