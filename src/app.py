import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table
from flask import Flask
import sys

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data import load_data
from callbacks import register_callbacks
from components import create_map
from calculate_arrivals_departures import calculate_arrivals_departures

server = Flask(__name__)

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load AIS dataset
df = load_data()

# Ensure consistent date format
df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime']).dt.strftime('%Y-%m-%d')

# Calculate Number of Arrivals & Departures per Port
df_port = calculate_arrivals_departures(df)

# Function to create Bootstrap-styled summary cards
def create_summary_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title"),
            html.H3(id=value, children="...", className="card-text", style={"fontWeight": "bold"})
        ]),
        style={"textAlign": "center", "margin": "10px", "backgroundColor": color, "color": "white"}
    )

# App layout
app.layout = dbc.Container([
    html.H1("🚢 AIS Unique Vessel Tracking", className="text-center my-4"),

    # Summary Metrics Row (Now Includes Maximum Time Anchored)
    dbc.Row([
        dbc.Col(create_summary_card("Total Unique Vessels", "total-unique-vessels", "#007BFF"), width=3),
        dbc.Col(create_summary_card("Total Moving Vessels", "total-moving-vessels", "#28A745"), width=3),
        dbc.Col(create_summary_card("Total Anchored Vessels", "total-anchored-vessels", "#DC3545"), width=3),
        dbc.Col(create_summary_card("Max Time Anchored (hours)", "max-time-anchored", "#FFC107"), width=3),
    ], className="justify-content-center my-3"),

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

        dbc.Col(dcc.Dropdown(
            id="vessel-name-filter",
            options=[{"label": name, "value": name} for name in df['VesselName'].dropna().unique()],
            placeholder="Select Vessel Name"
        ), width=3),

        dbc.Col(dcc.RadioItems(
            id="date-filter",
            options=[{"label": date, "value": date} for date in df['BaseDateTime'].dropna().unique()],
            value=df['BaseDateTime'].min(),
            inline=True
        ), width=3)
    ], className="my-3"),

    # Port data Section 
    dbc.Row([  
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H5("Number of Arrivals & Departures per Port", style={"fontFamily": "Arial, sans-serif"}),
                    dash_table.DataTable(
                        id="port-table",
                        columns=[{"name": col, "id": col} for col in df_port.columns],
                        data=df_port.to_dict("records"),
                        page_size=5, 
                        style_table={"overflowX": "auto", "margin":"auto", "border": "none", "fontFamily": "Arial, sans-serif"},
                        style_header={"fontWeight": "bold", "border": "none", "fontFamily": "Arial, sans-serif"},
                        style_cell={"textAlign": "center", "border": "none", "fontFamily": "Arial, sans-serif"},
                        style_data={"border": "none"}
                    )
                ])
            ), width=4
        ),

    # Map Section
        dbc.Col(dcc.Graph(id="map-output", style={'height': '60vh'}), width=8
        ),
    ], align="center")
], fluid=True)

# Register callbacks to update the map & summary stats
register_callbacks(app, df)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run_server(host="0.0.0.0", port=port)
