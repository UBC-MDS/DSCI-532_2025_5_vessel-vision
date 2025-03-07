
# main
import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table
from flask import Flask
import sys
import plotly.graph_objects as go

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
df = load_data(date_filter="2024-01-01")

# Ensure consistent date format
df['Hour'] = df['BaseDateTime'].dt.hour
df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime']).dt.strftime('%Y-%m-%d')

# Compute Port table
port_result_df, car_df, pas_df = calculate_arrivals_departures(df)

def create_port_table(port_result_df):
    """Create a Bootstrap Card containing the Port Table."""
    return dbc.Card(
        dbc.CardBody([ 
            html.H5("Number of Arrivals & Departures per Port", style={"fontFamily": "Arial, sans-serif"}),
            dash_table.DataTable(
                id="port-table",
                columns=[{"name": col, "id": col} for col in port_result_df.columns],
                data=port_result_df.to_dict("records"),
                page_size=4,
                style_table={"overflowX": "auto", "margin": "auto", "border": "none", "fontFamily": "Arial, sans-serif"},
                style_header={"fontWeight": "bold", "border": "none", "fontFamily": "Arial, sans-serif"},
                style_cell={"textAlign": "center", "border": "none", "fontFamily": "Arial, sans-serif"},
                style_data={"border": "none"}
            )
        ])
    )

# Function to create Bootstrap-styled summary cards
def create_summary_card(title, value, color):
    return dbc.Card(
        dbc.CardBody([ 
            html.H5(title, className="card-title"),
            html.H3(id=value, children="...", className="card-text", style={"fontWeight": "bold"})
        ]),
        style={"textAlign": "center", "margin": "10px", "backgroundColor": color, "color": "white"}
    )

# Function to create trend graph with dynamic height
def create_trend_graph(df):
    df_trend = df.groupby('Hour').size().reset_index(name='Unique Vessels')

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_trend['Hour'],
        y=df_trend['Unique Vessels'],
        mode='lines+markers',
        name='Unique Vessels Over Time',
        line=dict(color='blue')
    ))

    # Dynamically adjust height
    min_height = 150  
    max_height = 300  
    graph_height = min(max(len(df_trend) * 10, min_height), max_height)

    fig.update_layout(
        title='Trend of Unique Vessels Over Time',
        xaxis_title='Hour of the Day',
        yaxis_title='Number of Vessels',
        template='plotly_white',
        margin=dict(l=20, r=20, t=30, b=20),
        height=graph_height
    )

    return dcc.Graph(id="trend-graph", figure=fig, style={"height": "100%", "width": "100%"})

# Function to create the footer
def create_footer():
    return html.Footer(
        dbc.Container(
            dbc.Row(
                dbc.Col([
                    html.Hr(), 
                    html.P("Vessel Vision, extract and process AIS data for maritime traffic analysis.", className="text-center", style={"fontWeight": "bold","margin-bottom": "2px"}),
                    html.P("Developed by [DSCI-532-group5]: Azin Piran, Stephanie Wu, Yasmin Hassan, Zoe Ren", className="text-center",style={"margin-bottom": "2px"}),
                    html.P([
                        "GitHub Repository: ",
                        html.A("Vessel Vision", href="https://github.com/UBC-MDS/DSCI-532_2025_5_vessel-vision", target="_blank")
                    ], className="text-center",style={"margin-bottom": "2px"}),
                    html.P(f"Last updated: 2025-03-01", className="text-center",style={"margin-bottom": "2px"}),
                ])
            )
        ),
        style={
            "position": "relative",  
            "bottom": "0",
            "width": "100%",
            "padding": "0px",
            "backgroundColor": "#e9ecef",
            "textAlign": "center"
            #"borderTop": "1px solid #ccc"
        }
    )

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
            dcc.Graph(id="map-output", style={'height': '100%', 'margin': '0', 'padding': '0'}),
            width=7,
            style={"height": "55vh", "padding": "0", "backgroundColor": "#f0f0f0"}
        ),
    ], align="stretch", className="justify-content-center my-2"),

    # Footer
    create_footer()  # Ensure the footer is correctly included

], fluid=True, style={"backgroundColor": "#e9ecef", "minHeight": "100vh", "display": "flex", "flexDirection": "column", "justifyContent": "space-between"})

# Register callbacks
register_callbacks(app, df, port_result_df, car_df, pas_df)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run_server(host="0.0.0.0", port=port)

