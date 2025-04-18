from dash import Dash
from model.model_manager import ModelManager
from view.view_manager import ViewManager
from controller.controller_manager import ControllerManager

def create_app():
    """Create and configure the Dash application"""
    # Initialize the Dash app
    app = Dash(__name__)
    
    # Initialize managers
    model_manager = ModelManager()
    view_manager = ViewManager()
    
    # Set the layout
    app.layout = view_manager.create_layout()
    
    # Initialize controller
    controller = ControllerManager(app, model_manager, view_manager)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run_server(debug=True) 