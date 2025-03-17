import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html
from flask import Flask
from flask_caching import Cache  #  Added Flask Caching
import sys

# Add the current directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


# To make render faster

if "RENDER" in os.environ:
    from data import load_data
    from callbacks import register_callbacks
    from components import create_map, create_port_table, create_summary_card, create_trend_graph, create_footer
    from calculate_arrivals_departures import calculate_arrivals_departures
else:
    from data import load_data
    from callbacks import register_callbacks
    from components import create_map, create_port_table, create_summary_card, create_trend_graph, create_footer
    from calculate_arrivals_departures import calculate_arrivals_departures

server = Flask(__name__)

# Initialize caching (Using simple file-based cache)
cache = Cache(server, config={'CACHE_TYPE': 'simple', "CACHE_DEFAULT_TIMEOUT": 300})

# Initialize Dash app with Bootstrap theme
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the browser tab title
app.title = "Vessel Vision Dashboard"

# Caching dataset load (Pre-load once and cache for faster access)
@cache.cached(timeout=600, key_prefix='cached_df')
def get_cached_data():
    """
    This function loads the dataset with a date filter and caches it for 600 seconds.
    It allows faster access to the data without reloading from the source each time.
    """
    return load_data(date_filter="2024-01-01")

df = get_cached_data()  # Load cached data

# Ensure consistent date format
df['Hour'] = df['BaseDateTime'].dt.hour
df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime']).dt.strftime('%Y-%m-%d')

# Cache Port calculations
@cache.cached(timeout=600, key_prefix='cached_port_table')
def get_cached_port_table():
    """
    This function computes the port arrival and departure data from the provided dataframe.
    The result is cached for faster access on subsequent loads.
    """
    return calculate_arrivals_departures(df)

port_result_df, car_df, pas_df = get_cached_port_table()
port_table = create_port_table(port_result_df)

#  Cache trend graph
@cache.cached(timeout=600, key_prefix='cached_trend_graph')
def get_cached_trend_graph():
    """
    This function generates a trend graph from the dataframe and caches it for 600 seconds.
    It is used to quickly render the trend visualizations.
    """
    return create_trend_graph(df)

trend_graph = get_cached_trend_graph()

# Cache map to prevent re-rendering
@cache.cached(timeout=600, key_prefix='cached_map')
def get_cached_map():
    """
    This function creates and caches the map visualization for faster rendering.
    The map is based on the data provided in the dataframe.
    """
    return create_map(df)

map_section = dbc.Col(
    dcc.Graph(id="map-output", figure=get_cached_map(), style={'height': '100%', 'margin': '0', 'padding': '0'}),
    width=7,
    style={"height": "55vh", "padding": "0", "backgroundColor": "white"}
)

# Port Table & Trend Graph Section (Fixed height)
port_section = dbc.Col([ 
    html.Div(
        port_table,
        style={"height": "22vh",}
    ),
    html.Div(
        trend_graph,
        style={"height": "33vh"}
    )
], width=4, style={
    "height": "55vh",  
    "display": "flex", 
    "flexDirection": "column", 
    "justifyContent": "flex-start", 
})

# App layout
app.layout = dbc.Container([
    html.Div([
        html.H1([
            html.Span("🚢", style={"fontSize": "4rem", "marginRight": "2rem"}),  # Bigger left ship emoji
            "Vessel Vision",
            html.Span("🚢", style={"fontSize": "4rem", "marginLeft": "2rem"})   # Bigger right ship emoji
        ], className="text-center mb-0", style={"display": "flex", "justifyContent": "center", "alignItems": "center"}),
        html.H5("- AIS Unique Vessel Tracking -", className="text-center text-muted")
    ], className="my-2"),

    # Summary Metrics Row
    dbc.Row([
        dbc.Col(create_summary_card("Total Unique Vessels", "total-unique-vessels", "#007BFF"), width=3),
        dbc.Col(create_summary_card("Total Moving Vessels", "total-moving-vessels", "#28A745"), width=3),
        dbc.Col(create_summary_card("Total Anchored Vessels", "total-anchored-vessels", "#6F42C1"), width=3),
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
            options=[{"label": f" The data is from the date(s): {date}", "value": date} for date in df['BaseDateTime'].dropna().unique()],
            value=df['BaseDateTime'].min(),
            inline=True
        ), width=3)
    ], className="justify-content-center my-2"),

    # Port Data Section with Trend Graph
    dbc.Row([
        port_section,
        map_section
    ], align="stretch", className="justify-content-center my-2"),

    # Footer
    create_footer() 

], fluid=True, style={"backgroundColor": "white", "minHeight": "100vh", "display": "flex", "flexDirection": "column", "justifyContent": "space-between"})

# Register callbacks
register_callbacks(app, df, port_result_df, car_df, pas_df)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run_server(host="0.0.0.0", port=port)
