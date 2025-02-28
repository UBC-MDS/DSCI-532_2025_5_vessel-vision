import os
import pandas as pd
from dash import Dash, dcc, html
from flask import Flask
import sys

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data import load_data
from callbacks import register_callbacks
from components import create_map

server = Flask(__name__)

# Initialize the Dash app
app = Dash(__name__, server=server)

# Load AIS dataset using the data.py module
df = load_data()

# Ensure the date format is consistent in 'yyyy-mm-dd' format
df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime']).dt.strftime('%Y-%m-%d')

# Initialize layout
app.layout = html.Div([
    html.H1("AIS Unique Vessel Tracking", style={'textAlign': 'center', 'padding': '20px'}),

    # Container for filters at the top (all in one row)
    html.Div([
        # Vessel Type Filter (Dropdown)
        dcc.Dropdown(
            id="vessel-type-filter",
            options=[{"label": vessel_type, "value": vessel_type} for vessel_type in df['Vessel Type Name'].dropna().unique()],
            placeholder="Select Vessel Type",
            style={'width': '18%', 'padding': '10px', 'display': 'inline-block'}
        ),

        # Nearest Port Filter (Dropdown)
        dcc.Dropdown(
            id="nearest-port-filter",
            options=[{"label": port, "value": port} for port in df['Nearest Port'].dropna().unique()],
            placeholder="Select Nearest Port",
            style={'width': '18%', 'padding': '10px', 'display': 'inline-block'}
        ),

        # Vessel Name Filter (Dropdown)
        dcc.Dropdown(
            id="vessel-name-filter",
            options=[{"label": name, "value": name} for name in df['VesselName'].dropna().unique()],
            placeholder="Select Vessel Name",
            style={'width': '18%', 'padding': '10px', 'display': 'inline-block'}
        ),

        # Date Filter (Radio Button)
        dcc.RadioItems(
            id="date-filter",
            options=[{"label": date, "value": date} for date in df['BaseDateTime'].dropna().unique()],
            value=df['BaseDateTime'].min(),  # Set default to the earliest date
            style={'width': '18%', 'padding': '10px', 'display': 'inline-block'}
        )
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'padding': '20px', 'flexWrap': 'wrap'}),  # Filters in one line

    # Map section with reduced size and centered
    html.Div([
        dcc.Graph(id="map-output", style={'height': '50vh', 'width': '60%'})  # Smaller map size
    ], style={'display': 'flex', 'justifyContent': 'center', 'padding': '10px'}),  # Center the map
])

# Register callbacks to make the app interactive
register_callbacks(app, df)

if __name__ == '__main__':
    # Run the Dash app
    port = int(os.environ.get("PORT", 10000))  # Get PORT from Render or default to 10000
    app.run_server(host="0.0.0.0", port=port)

