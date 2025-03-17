from dash.dependencies import Input, Output
import os
import sys
import pandas as pd
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from components import create_map
from calculate_arrivals_departures import calculate_arrivals_departures

def register_callbacks(app, df, port_result_df, car_df, pas_df):
    """
    Register the callbacks for the Dash app to update the map, statistics, 
    and trend graph based on user input.
    
    Args:
        app (dash.Dash): The Dash app instance.
        df (pd.DataFrame): The main dataframe containing vessel data.
        port_result_df (pd.DataFrame): DataFrame containing port-related results.
        car_df (pd.DataFrame): DataFrame containing cargo vessel data.
        pas_df (pd.DataFrame): DataFrame containing passenger vessel data.
    
    Returns:
        None: This function does not return anything. It registers callbacks 
              with the Dash app.
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
        """
        Update the map and various statistics based on the selected filters.
        
        Args:
            vessel_type (str): Selected vessel type to filter by.
            nearest_port (str): Selected port to filter by.
            selected_date (str): Selected date to filter by.
        
        Returns:
            tuple: Contains updated map figure, port table data, and various 
                   statistics (total unique vessels, moving vessels, anchored 
                   vessels, and max time anchored).
        """
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
            filtered_df["Duration Anchored"] = pd.to_timedelta(filtered_df["Duration Anchored"], errors='coerce')
            max_time_anchored = filtered_df["Duration Anchored"].max()
            max_time_anchored = f"{round(max_time_anchored.total_seconds() / 3600, 2)} hours" if pd.notna(max_time_anchored) else "N/A"
        else:
            max_time_anchored = "N/A"  # If column doesn't exist
        

        # Fix: For Port table, compute from port_result_df rather than calculate again
        if vessel_type == "Cargo":
            selected_df = car_df
        elif vessel_type == "Passenger":
            selected_df = pas_df
        else:
            selected_df = port_result_df

        if nearest_port:
            selected_df = selected_df[selected_df["PORT NAME"] == nearest_port]

        return create_map(filtered_df), selected_df.to_dict("records"), f"{total_unique_vessels:,}", f"{total_moving_vessels:,}", f"{total_anchored_vessels:,}", max_time_anchored


    @app.callback(
        Output("trend-graph", "figure"),  # Ensure your Graph component has id="trend-graph"
        [
            Input("vessel-type-filter", "value"),
            Input("nearest-port-filter", "value"),
            Input("date-filter", "value")
        ]
    )
    def update_trend_graph(vessel_type, nearest_port, selected_date):
        """
        Update the trend graph based on selected filters. Dynamically adjusts the 
        graph height based on the amount of data being visualized.
        
        Args:
            vessel_type (str): Selected vessel type to filter by.
            nearest_port (str): Selected port to filter by.
            selected_date (str): Selected date to filter by.
        
        Returns:
            plotly.graph_objects.Figure: The updated figure for the trend graph.
        """
        filtered_df = df.copy()

        if vessel_type:
            filtered_df = filtered_df[filtered_df["Vessel Type Name"] == vessel_type]

        if nearest_port:
            filtered_df = filtered_df[filtered_df["Nearest Port"] == nearest_port]

        if selected_date:
            filtered_df = filtered_df[filtered_df["BaseDateTime"] == selected_date]

        df_trend = filtered_df.groupby('Hour').size().reset_index(name='Unique Vessels')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_trend['Hour'],
            y=df_trend['Unique Vessels'],
            mode='lines+markers',
            name='Unique Vessels Over Time',
            line=dict(color='blue')
        ))

        # Dynamically adjust height
        default_height = 250  # Default height
        if len(df_trend) < 10:
            graph_height = 200  # Reduce height for small data
        elif len(df_trend) > 20:
            graph_height = 300  # Expand height for large data
        else:
            graph_height = default_height  # Keep default

        fig.update_layout(
            title='Trend of Unique Vessels Over Time',
            xaxis_title='Hour of the Day',
            yaxis_title='Number of Vessels',
            template='plotly_white',
            margin=dict(l=20, r=20, t=30, b=20),
            height=graph_height  # Dynamically adjust height
        )

        return fig
