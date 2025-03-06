import os
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, dash_table
from flask import Flask
import plotly.graph_objects as go
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
df = load_data(date_filter="2024-01-01")

# Ensure consistent date format
df['Hour'] = df['BaseDateTime'].dt.hour
df['BaseDateTime'] = pd.to_datetime(df['BaseDateTime']).dt.strftime('%Y-%m-%d')

# Function to create Bootstrap-styled Port table
df_port = calculate_arrivals_departures(df)

def create_port_table(df_port):
    """Create a Bootstrap Card containing the Port Table."""
    vessel_types = df['Vessel Type Name'].dropna().unique()
    
    # Creating a list of Vessel Type Name and its color (this could be customized)
    vessel_type_colors = {
        "Cargo": "#FF6347",
        "Fishing": "#4682B4",
        "Passenger": "#32CD32",
        "Tanker": "#FFD700"
    }
    
    # Adding color information to the header
    header_cells = [
        {
            "name": f"Vessel Type Name ({vessel_type})",
            "id": vessel_type,
            "style": {
                "backgroundColor": vessel_type_colors.get(vessel_type, "#808080"),  # Default gray if type is missing
                "color": "white",
                "fontWeight": "bold"
            }
        }
        for vessel_type in vessel_types
    ]
    
    return dbc.Card(
        dbc.CardBody([ 
            html.H5("Number of Arrivals & Departures per Port", style={"fontFamily": "Arial, sans-serif"}),
            dash_table.DataTable(
                id="port-table",
                columns=[{"name": col, "id": col} for col in df_port.columns],
                data=df_port.to_dict("records"),
                page_size=5,
                style_table={"overflowX": "auto", "margin": "auto", "border": "none", "fontFamily": "Arial, sans-serif"},
                style_header={
                    "fontWeight": "bold", 
                    "border": "none", 
                    "fontFamily": "Arial, sans-serif",
                    "backgroundColor": "#D3D3D3",  # Light gray background for header
                },
                style_cell={ 
                    "textAlign": "center", 
                    "border": "none", 
                    "fontFamily": "Arial, sans-serif"
                },
                style_data={"border": "none"},
                style_header_conditional=header_cells  # Apply conditional styling for coloring
            )
        ]),
        style={
            "flex": "1", "display": "flex", "flexDirection": "column"  
        }
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

# Footer of dashboard
def create_footer():
    return dbc.Container(
        dbc.Row(
            dbc.Col([ 
                html.Hr(), 
                html.P("Vessel Vision, extract and process AIS data for maritime traffic analysis.", className="text-center", style={"fontWeight": "bold"}),
                html.P("Developed by [DSCI-532-group5]: Azin Piran, Stephanie Wu, Yasmin Hassan, Zoe Ren", className="text-center"),
                html.P([ 
                    "GitHub Repository: ",
                    html.A("Vessel Vision", href="https://github.com/UBC-MDS/DSCI-532_2025_5_vessel-vision", target="_blank")
                ], className="text-center"),
                html.P(f"Last updated: 2025-03-01 ", className="text-center"),
            ])
        ), className="mt-4"
    )

# Add a trend line graph function
def create_trend_graph(df):
    # Example: Trend of total unique vessels over time
    df_trend = df.groupby('Hour').size().reset_index(name='Unique Vessels')
    trend_graph = go.Figure()
    trend_graph.add_trace(go.Scatter(
        x=df_trend['Hour'],
        y=df_trend['Unique Vessels'],
        mode='lines+markers',
        name='Unique Vessels Over Time',
        line=dict(color='blue')
    ))
    trend_graph.update_layout(
        title='Trend of Unique Vessels Over Time',
        xaxis_title='Hour of the Day',
        yaxis_title='Number of Vessels',
        template='plotly_white'
    )

    # Return the graph inside a dbc.Card to ensure proper layout handling
    return dbc.Card(
        dbc.CardBody([
            dcc.Graph(
                figure=trend_graph,
                style={
                    'height': '100%',
                    'width': '100%',
                    'border': '1px solid #ccc',  # Light border
                    'borderRadius': '5px',  # Slightly rounded corners
                    'padding': '5px'  # Padding inside the border
                }
            )
        ]),
        style={"flex": "1", "display": "flex", "flexDirection": "column"}  # Expands to fill space
    )


# App layout
###################################################################################################################################
# App layout
app.layout = dbc.Container([ 
    html.H1("Vessel Vision - 🚢 AIS Unique Vessel Tracking", className="text-center my-4"),

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

        dbc.Col(dcc.RadioItems(
            id="date-filter",
            options=[{"label": date, "value": date} for date in df['BaseDateTime'].dropna().unique()],
            value=df['BaseDateTime'].min(),
            inline=True
        ), width=3)
    ], className="my-3"),

    # Port Data Section with Trend Graph Below the Table
    dbc.Row([ 
        dbc.Col([ 
            create_port_table(df_port),  # Port table
            create_trend_graph(df),      # Trend graph below table
        ], width=4, style={
            "height": "70vh", 
            "display": "flex", 
            "flexDirection": "column", 
            "justifyContent": "flex-start"}),  # Port table and trend graph in first column

        # Map Section with border and light gray header
        dbc.Col(
            dcc.Graph(
                id="map-output", 
                style={
                    'height': '100%',  # Ensure full height for the map
                    'border': '1px solid #ccc',  # Add light border
                    'borderRadius': '1px',  # Light border radius for rounded corners
                    'padding': 0  # Remove any padding around the map
                },
                figure={
                    'data': create_map(df),  # Replace with actual map data (without color coding by vessel type)
                    'layout': {
                        'showlegend': False,  # Disable the legend
                        'height': 850,  # Set height of the map
                        'margin': {'r': 0, 't': 0, 'b': 0, 'l': 0}  # Remove margin
                    }
                }
            ), 
            width=8,
            style={"height": "70vh", "paddingleft": 0,"paddingRight": "20px", "backgroundColor": "#f0f0f0"}  # Background color for map section
        ),
    ], align="stretch", className="my-3"),

    # Footer section
    create_footer()

], fluid=True, style={"backgroundColor": "#e9ecef"})  # Background color for the entire container


#######################################################################################################################################
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run_server(host="0.0.0.0", port=port)
