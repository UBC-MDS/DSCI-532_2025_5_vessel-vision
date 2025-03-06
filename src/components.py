# # Placeholder for reusable components

# import plotly.express as px

# def create_filters(vessel_types, nearest_ports, vessel_names, dates):
#     """
#     This function will create all the filters: dropdowns for vessel type, nearest port, vessel name,
#     and radio button for date.
#     """
#     return html.Div([
#         dcc.Dropdown(
#             id="vessel-type-filter",
#             options=[{"label": vt, "value": vt} for vt in vessel_types],
#             placeholder="Select Vessel Type",
#         ),
#         dcc.Dropdown(
#             id="nearest-port-filter",
#             options=[{"label": np, "value": np} for np in nearest_ports],
#             placeholder="Select Nearest Port",
#         ),
#         dcc.Dropdown(
#             id="vessel-name-filter",
#             options=[{"label": vn, "value": vn} for vn in vessel_names],
#             placeholder="Select Vessel Name",
#         ),
#         dcc.RadioItems(
#             id="date-filter",
#             options=[{"label": dt, "value": dt} for dt in dates],
#             labelStyle={"display": "inline-block"},
#         ),
#     ], style={'display': 'flex', 'gap': '10px'})

# def create_map(filtered_df):
#     """
#     This function generates a map with the filtered DataFrame.
#     It also adds summary information (total unique vessels) to the map title and as an annotation.
#     """
#     # Calculate the total number of unique vessels based on MMSI
#     unique_count = filtered_df["MMSI"].nunique()
    
#     # Create the map figure using Plotly Express
#     fig = px.scatter_mapbox(
#         filtered_df,
#         lat="LAT",
#         lon="LON",
#         color="Vessel Type Name",
#         hover_data=["MMSI", "VesselName", "SOG"],
#         mapbox_style="open-street-map",
#         zoom=5,
#         size_max=10
#     )
    
#     # Add an annotation with the unique vessel count (optional)
#     fig.add_annotation(
#         text=f"Total Unique Vessels: {unique_count}",
#         xref="paper", yref="paper",
#         x=0.05, y=0.95,  # Position near the top-left of the map
#         showarrow=False,
#         font=dict(size=14, color="black")
#     )
    
#     return fig


# Placeholder for reusable components

import plotly.express as px
from dash import html, dcc

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
    # Calculate the total number of unique vessels based on MMSI
    unique_count = filtered_df["MMSI"].nunique()
    
    # Create the map figure using Plotly Express
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
    
    # Add an annotation with the unique vessel count (optional)
    fig.add_annotation(
        text=f"Total Unique Vessels: {unique_count}",
        xref="paper", yref="paper",
        x=0.05, y=0.95,  # Position near the top-left of the map
        showarrow=False,
        font=dict(size=14, color="black")
    )

    # ✅ Move the legend to the bottom center
    fig.update_layout(
        legend=dict(
            orientation="h",  # Make legend horizontal
            yanchor="bottom",  # Align legend at the bottom
            y=-0.05,  # Move legend slightly below the map
            xanchor="center",  # Center-align legend
            x=0.5  # Place legend in the middle
        ),
        margin=dict(r=0, t=0, l=0, b=20)  # Remove extra margins around the map
    )
    
    return fig

