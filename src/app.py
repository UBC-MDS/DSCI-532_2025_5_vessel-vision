import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html

# Initialize the Dash app
app = Dash(__name__)

# Load AIS dataset
data_path = "data/processed/ais_west_coast.csv"
df = pd.read_csv(data_path)

# Keep only the latest record per vessel (MMSI) to show unique vessels
df_unique = df.sort_values(by="BaseDateTime", ascending=False).drop_duplicates(subset="MMSI")

# Create map visualization
fig = px.scatter_mapbox(
    df_unique,
    lat="LAT",
    lon="LON",
    color="VesselType",  # Different colors for different vessel types
    hover_data=["MMSI", "VesselName", "SOG", "COG", "Heading"],
    title="AIS Unique Vessel Positions",
    mapbox_style="open-street-map",
    zoom=5,  # Adjust zoom level as needed
    size_max=10  # Increase marker size
)

# Layout with increased size for the scatter plot
app.layout = html.Div([
    html.H1("AIS Unique Vessel Tracking"),
    dcc.Graph(
        figure=fig,
        style={'height': '80vh', 'width': '100%'}  # Increased size for the plot
    )
])

# Run the app/dashboard
if __name__ == '__main__':
    app.run(debug=True)
