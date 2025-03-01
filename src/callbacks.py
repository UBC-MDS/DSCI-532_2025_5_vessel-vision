from dash.dependencies import Input, Output
import os
import sys
import pandas as pd

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from components import create_map
from calculate_arrivals_departures import calculate_arrivals_departures

def register_callbacks(app, df):
    """
    This function registers the callbacks for the app.
    """

    @app.callback(
        [
            Output("map-output", "figure"), 
            Output("port-table", "data"),
            Output("total-unique-vessels", "children"),
            Output("total-moving-vessels", "children"),
            Output("total-anchored-vessels", "children"),
            Output("max-time-anchored", "children")
        ],
        [
            Input("vessel-type-filter", "value"),
            Input("nearest-port-filter", "value"),
            Input("date-filter", "value")
        ]
    )
    def update_map_and_stats(vessel_type, nearest_port, selected_date):
        # Start with the full dataframe
        filtered_df = df.copy()

        # Apply Vessel Type filter
        if vessel_type:
            filtered_df = filtered_df[filtered_df["Vessel Type Name"] == vessel_type]

        # Apply Nearest Port filter
        if nearest_port:
            filtered_df = filtered_df[filtered_df["Nearest Port"] == nearest_port]


        # Apply Date filter
        if selected_date:
            filtered_df = filtered_df[filtered_df["BaseDateTime"] == selected_date]

        # Compute updated metrics
        total_unique_vessels = filtered_df["MMSI"].nunique()
        total_moving_vessels = filtered_df[filtered_df["SOG"] > 0]["MMSI"].nunique()
        total_anchored_vessels = filtered_df[filtered_df["SOG"] == 0]["MMSI"].nunique()

        # Ensure 'Duration Anchored' is in a consistent numeric format (Timedelta or hours as float)
        if "Duration Anchored" in filtered_df.columns:
        # Convert to Timedelta if not already, or convert to hours as a float
            filtered_df["Duration Anchored"] = pd.to_timedelta(filtered_df["Duration Anchored"], errors='coerce')
        # Get the maximum time anchored in hours
            max_time_anchored = filtered_df["Duration Anchored"].max()
            if pd.isna(max_time_anchored):
                max_time_anchored = "N/A"  # If there's no valid time
            else:
                max_time_anchored = round(max_time_anchored.total_seconds() / 3600, 2)  # Convert to hours
        else:
            max_time_anchored = "N/A"  # If column doesn't exist
        
        # return updated Port table calculation(arrivals and departures)
        port_table_df = calculate_arrivals_departures(filtered_df)

    # Return updated data
        return create_map(filtered_df), port_table_df.to_dict("records"), f"{total_unique_vessels:,}", f"{total_moving_vessels:,}", f"{total_anchored_vessels:,}", f"{max_time_anchored} hours"
