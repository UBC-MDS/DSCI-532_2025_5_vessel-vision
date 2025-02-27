# Placeholder for callbacks, if needed for interactivity later
import os
from dash.dependencies import Input, Output

import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components import create_map

def register_callbacks(app, df):
    """
    This function registers the callbacks for the app.
    """
    @app.callback(
        Output("map-output", "figure"),  # Output is the map figure
        [
            Input("vessel-type-filter", "value"),  # Vessel Type Filter
            Input("nearest-port-filter", "value"),  # Nearest Port Filter
            Input("vessel-name-filter", "value"),  # Vessel Name Filter
            Input("date-filter", "value")  # Date Filter (Radio Button)
        ]
    )
    def update_map(vessel_type, nearest_port, vessel_name, selected_date):
        # Start with the full dataframe
        filtered_df = df.copy()

        # Apply Vessel Type filter
        if vessel_type:
            filtered_df = filtered_df[filtered_df["VesselType"] == vessel_type]
        
        # Apply Nearest Port filter
        if nearest_port:
            filtered_df = filtered_df[filtered_df["NearestPort"] == nearest_port]
        
        # Apply Vessel Name filter
        if vessel_name:
            filtered_df = filtered_df[filtered_df["VesselName"] == vessel_name]
        
        # Apply Date filter
        if selected_date:
            filtered_df = filtered_df[filtered_df["BaseDateTime"] == selected_date]

        # Return updated map figure
        return create_map(filtered_df)
