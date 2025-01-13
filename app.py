import streamlit as st
import folium
import geopandas as gpd
from folium import plugins
from streamlit_folium import st_folium

# Helper function to filter GeoDataFrame based on a column and value
def filter_gdf(gdf, column, value):
    return gdf[gdf[column] == value]

# Helper function to get valid tooltip fields
def get_valid_tooltip_fields(gdf):
    # Use the first two columns as fields if available
    if len(gdf.columns) >= 2:
        fields = list(gdf.columns[:2])
        aliases = list(gdf.columns[:2])
    elif len(gdf.columns) == 1:
        fields = [gdf.columns[0]]
        aliases = [gdf.columns[0]]
    else:
        fields, aliases = [], []
    return fields, aliases

# Streamlit Sidebar for user input controls
st.sidebar.header("Interactive Controls")

# Road Type Selection
road_types = ['All', 'Primary', 'Secondary', 'Tertiary']
selected_road_type = st.sidebar.selectbox("Select Road Type", road_types)

# Urban Density Selection
density_levels = ['All', 'Low', 'Medium', 'High']
selected_density = st.sidebar.selectbox("Select Urban Density", density_levels)

# Timeframe Selection for Vegetation Data
timeframes = ['All Time', 'Recent']
selected_timeframe = st.sidebar.selectbox("Select Vegetation Timeframe", timeframes)

# Load GeoJSON files
data_files = {
    "Land Use": "data/Land_Use.geojson",
    "Local Climate Zones": "data/LCZ.GeoJson.geojson",
    "Vegetation Distribution (NDVI)": "data/NDVI-DS.geojson",
    "Roads": "data/Roads.geojson",
    "Urban Density": "data/UrbanDensity.geojson"
}

# Initialize Map (No fixed center, will update dynamically later)
m = folium.Map()

# Add layers with filtering and tooltips
for name, path in data_files.items():
    gdf = gpd.read_file(path)
    
    # Apply specific filters based on user selection
    if name == "Roads" and selected_road_type != "All":
        gdf = filter_gdf(gdf, "highway", selected_road_type)
    elif name == "Urban Density" and selected_density != "All":
        gdf = filter_gdf(gdf, "density_level", selected_density)
    elif name == "Vegetation Distribution (NDVI)" and selected_timeframe != "All Time":
        gdf = gdf[gdf["timeframe"] == selected_timeframe]

    # Ensure valid tooltip fields
    fields, aliases = get_valid_tooltip_fields(gdf)

    # Add GeoJSON layer with tooltips
    layer = folium.GeoJson(
        gdf,
        name=name,
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases) if fields else None
    )
    layer.add_to(m)

    # Update map's center and zoom level based on the bounds of the current dataset
    minx, miny, maxx, maxy = gdf.total_bounds
    map_center = [(miny + maxy) / 2, (minx + maxx) / 2]  # Center the map in the middle of the dataset
    m.fit_bounds([[miny, minx], [maxy, maxx]])  # Fit the map to the dataset bounds

# Add Layer Control
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st_data = st_folium(m, width=900, height=600)












