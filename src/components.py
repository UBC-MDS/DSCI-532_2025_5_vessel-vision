import plotly.express as px
from dash import html, dcc, dash_table
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

def create_filters(vessel_types, nearest_ports, vessel_names, dates):
    """
    This function will create all the filters: dropdowns for vessel type, nearest port, vessel name,
    and radio button for date.
    """
    return html.Div([
        dcc.Dropdown(
            id="vessel-type-filter",
            options=[{"label": vt, "value": vt} for vt in vessel_types],
            placeholder="Select Vessel Type",
        ),
        dcc.Dropdown(
            id="nearest-port-filter",
            options=[{"label": np, "value": np} for np in nearest_ports],
            placeholder="Select Nearest Port",
        ),
        dcc.Dropdown(
            id="vessel-name-filter",
            options=[{"label": vn, "value": vn} for vn in vessel_names],
            placeholder="Select Vessel Name",
        ),
        dcc.RadioItems(
            id="date-filter",
            options=[{"label": dt, "value": dt} for dt in dates],
            labelStyle={"display": "inline-block"},
        ),
    ], style={'display': 'flex', 'gap': '10px'})

def create_map(filtered_df):
    """
    This function generates a map with the filtered DataFrame.
    It also adds summary information (total unique vessels) to the map title and as an annotation.
    """
    unique_count = filtered_df["MMSI"].nunique()
    
    fig = px.scatter_mapbox(
        filtered_df,
        lat="LAT",
        lon="LON",
        color="Vessel Type Name",
        hover_data=["MMSI", "VesselName", "SOG"],
        mapbox_style="open-street-map",
        zoom=5,
        size_max=10
    )
    
    fig.add_annotation(
        text=f"Total Unique Vessels: {unique_count}",
        xref="paper", yref="paper",
        x=0.05, y=0.95,  # Position near the top-left of the map
        showarrow=False,
        font=dict(size=14, color="black")
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.05,
            xanchor="center",
            x=0.5
        ),
        margin=dict(r=0, t=0, l=0, b=20)
    )
    
    return fig

# Country names dictionary for hover tooltips
COUNTRY_NAMES = {
    "🇺🇸": "United States",
    "🇨🇦": "Canada",
    "🇲🇽": "Mexico",
    "🇬🇧": "United Kingdom",
    "🇯🇵": "Japan",
    "🇨🇳": "China",
    "🇩🇪": "Germany",
    "🇫🇷": "France",
    "🇮🇳": "India",
}

def create_port_table(port_result_df):
    """Create a Bootstrap Card containing the Port Table with hover tooltips."""
    return dbc.Card(
        dbc.CardBody([
            html.H5("Number of Arrivals & Departures per Port", style={"fontFamily": "Arial, sans-serif"}),
            dash_table.DataTable(
                id="port-table",
                columns=[
                    {"name": "FLAG", "id": "FLAG", "presentation": "markdown"},
                    {"name": "PORT NAME", "id": "PORT NAME"},
                    {"name": "ARRIVALS", "id": "ARRIVALS"},
                    {"name": "DEPARTURES", "id": "DEPARTURES"},
                ],
                data=port_result_df.to_dict("records"),
                page_size=3,

                # Add hover tooltips for FLAG column

                tooltip_data=[
                    {
                        "FLAG": {"value": COUNTRY_NAMES.get(row["FLAG"], "Unknown Country"), "type": "markdown"}
                    } for row in port_result_df.to_dict("records")
                ],
                tooltip_delay=0,
                tooltip_duration=None,
                style_table={"overflowX": "auto", "margin": "auto", "border": "none", "fontFamily": "Arial, sans-serif"},
                style_header={"fontWeight": "bold", "border": "none", "fontFamily": "Arial, sans-serif"},
                style_cell={
                    "textAlign": "center", 
                    "border": "none", 
                    "fontFamily": "Arial, sans-serif",
                    "padding": "1px",  
                    "margin": "0px",   
                    "lineHeight": "1" 
                },
                style_data={
                    "border": "none",
                    "height": "10px",  
                    "lineHeight": "1"
                },
                style_data_conditional=[
                    {
                        "if": {"row_index": "all"},
                        "padding": "1px",
                        "height": "10px",
                        "lineHeight": "1"
                    }
                ],
                css=[{
                    'selector': '.dash-spreadsheet tr',
                    'rule': 'line-height: 1 !important; height: 10px !important;'
                }]
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

# Function to create trend graph
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

    fig.update_layout(
        title='',
        xaxis_title='Hour of the Day',
        yaxis_title='Number of Vessels',
        template='plotly_white',
        margin=dict(l=50, r=20, t=30, b=20),
        font=dict(family="Arial, sans-serif"),  
        plot_bgcolor='white', 
        autosize=True
    )

    return dcc.Graph(
        id="trend-graph",
        figure=fig,
        config={"responsive": True},
        style={"height": "100%", "width": "100%", "border": "none"}
    )

# Function to create the footer
def create_footer():
    return html.Footer(
        dbc.Container(
            dbc.Row(
                dbc.Col([
                    html.Hr(), 

                    html.P("Vessel Vision, extract and process AIS data for maritime traffic analysis.", className="text-center", style={"fontWeight": "bold","margin-bottom": "2px"}),
                    html.P("Developed by Vessel vision Team: Azin Piran, Stephanie Wu, Yasmin Hassan, Zoe Ren", className="text-center",style={"margin-bottom": "2px"}),

                    html.P([
                        "GitHub Repository: ",

                        html.A("Vessel Vision", href="https://github.com/UBC-MDS/DSCI-532_2025_5_vessel-vision", target="_blank"),
                        ",    Last updated: 2025-03-16"
                    ], className="text-center", style={"margin-bottom": "2px"})

                ])
            )
        ),
        style={
            "position": "relative",  
            "bottom": "0",
            "width": "100%",
            "padding": "0px",
            "backgroundColor": "#fafafa",
            "textAlign": "center"
        }
    )
