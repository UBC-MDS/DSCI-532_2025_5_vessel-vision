import os
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
from flask import Flask
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data import load_data

server = Flask(__name__)

app = Dash(__name__, server=server)

# Load AIS dataset using the data.py module
df = load_data()

# Keep only the latest record per vessel (MMSI) to show unique vessels
df_unique = df.sort_values(by="BaseDateTime", ascending=False).drop_duplicates(subset="MMSI")

# Create map visualization
fig = px.scatter_mapbox(
    df_unique,
    lat="LAT",
    lon="LON",
    color="VesselType",
    hover_data=["MMSI", "VesselName", "SOG", "COG", "Heading"],
    title="AIS Unique Vessel Positions",
    mapbox_style="open-street-map",
    zoom=5,
    size_max=10
)

# Layout with increased size for the scatter plot
app.layout = html.Div([
    html.H1("AIS Unique Vessel Tracking"),
    dcc.Graph(
        figure=fig,
        style={'height': '80vh', 'width': '100%'}
    )
])

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Get PORT from Render
    app.run_server(host="0.0.0.0", port=port)
