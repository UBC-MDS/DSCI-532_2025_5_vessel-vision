
# main
import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table
import sys
import plotly.graph_objects as go

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data import load_data
from callbacks import register_callbacks
from components import create_map, create_trend_graph, create_summary_card, create_footer, create_port_table
from calculate_arrivals_departures import calculate_arrivals_departures

app = Dash(__name__)
server = app.server

# Load AIS dataset
df = load_data(date_filter="2024-01-01")

# Ensure consistent date format
df['Hour'] = df['BaseDateTime'].dt.hour
df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime']).dt.strftime('%Y-%m-%d')

# Compute Port table
port_result_df, car_df, pas_df = calculate_arrivals_departures(df)

# App layout
app.layout = dbc.Container([
    html.H1("Vessel Vision - 🚢 AIS Unique Vessel Tracking", className="text-center my-2"),

    # Summary Metrics Row
    dbc.Row([
        dbc.Col(create_summary_card("Total Unique Vessels", "total-unique-vessels", "#007BFF"), width=3),
        dbc.Col(create_summary_card("Total Moving Vessels", "total-moving-vessels", "#28A745"), width=3),
        dbc.Col(create_summary_card("Total Anchored Vessels", "total-anchored-vessels", "#DC3545"), width=3),
        dbc.Col(create_summary_card("Max Time Anchored (hours)", "max-time-anchored", "#FFC107"), width=3),
    ], className="justify-content-center my-2"),

    # Filters Section
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id="vessel-type-filter",
            options=[{"label": vessel_type, "value": vessel_type} for vessel_type in df['Vessel Type Name'].dropna().unique()],
            placeholder="Select Vessel Type"
        ), width=3),

        dbc.Col(dcc.Dropdown(
            id="nearest-port-filter",
            options=[{"label": port, "value": port} for port in df['Nearest Port'].dropna().unique()],
            placeholder="Select Nearest Port"
        ), width=3),

        dbc.Col(dcc.RadioItems(
            id="date-filter",
            options=[{"label": date, "value": date} for date in df['BaseDateTime'].dropna().unique()],
            value=df['BaseDateTime'].min(),
            inline=True
        ), width=3)
    ], className="justify-content-center my-2"),

    # Port Data Section with Trend Graph
    dbc.Row([
        dbc.Col([ 
            create_port_table(port_result_df),
            create_trend_graph(df),  
        ], width=4, style={"height": "55vh", "display": "flex", "flexDirection": "column", "justifyContent": "flex-start","overflowY": "auto" }),

        # Map Section
        dbc.Col(
            dcc.Graph(id="map-output", figure=create_map(df)),
            width=7,
            style={"height": "55vh", 'margin': '0', "padding": "0", "backgroundColor": "#f0f0f0"}
        ),
    ], align="stretch", className="justify-content-center my-2"),

    # Footer
    create_footer()  

], fluid=True, style={"backgroundColor": "#e9ecef", "minHeight": "100vh", "display": "flex", "flexDirection": "column", "justifyContent": "space-between"})

# Register callbacks
register_callbacks(app, df, port_result_df, car_df, pas_df)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run_server(host="0.0.0.0", port=port)

