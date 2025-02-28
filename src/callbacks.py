from dash.dependencies import Input, Output
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from components import create_map

def register_callbacks(app, df):
    """
    This function registers the callbacks for the app.
    """

    @app.callback(
        [
            Output("map-output", "figure"), 
            Output("total-unique-vessels", "children"),
            Output("total-moving-vessels", "children"),
            Output("total-anchored-vessels", "children"),
            Output("max-time-anchored", "children")
        ],
        [
            Input("vessel-type-filter", "value"),
            Input("nearest-port-filter", "value"),
            Input("vessel-name-filter", "value"),
            Input("date-filter", "value")
        ]
    )
    def update_map_and_stats(vessel_type, nearest_port, vessel_name, selected_date):
        # Start with the full dataframe
        filtered_df = df.copy()

        # Apply Vessel Type filter
        if vessel_type:
            filtered_df = filtered_df[filtered_df["Vessel Type Name"] == vessel_type]

        # Apply Nearest Port filter
        if nearest_port:
            filtered_df = filtered_df[filtered_df["Nearest Port"] == nearest_port]

        # Apply Vessel Name filter
        if vessel_name:
            filtered_df = filtered_df[filtered_df["VesselName"] == vessel_name]

        # Apply Date filter
        if selected_date:
            filtered_df = filtered_df[filtered_df["BaseDateTime"] == selected_date]

        # Compute updated metrics
        total_unique_vessels = filtered_df["MMSI"].nunique()
        total_moving_vessels = filtered_df[filtered_df["SOG"] > 0]["MMSI"].nunique()
        total_anchored_vessels = filtered_df[filtered_df["SOG"] == 0]["MMSI"].nunique()

        #Compute Maximum Time Anchored (if vessel was anchored)
        if "Duration Anchored" in filtered_df.columns:
            max_time_anchored = filtered_df["Duration Anchored"].max()
        else:
            max_time_anchored = "N/A"  # If column doesn't exist

        return create_map(filtered_df), f"{total_unique_vessels:,}", f"{total_moving_vessels:,}", f"{total_anchored_vessels:,}", f"{max_time_anchored} hours"
