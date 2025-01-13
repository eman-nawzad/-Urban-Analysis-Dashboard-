import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Set Streamlit page configuration
st.set_page_config(page_title="Urban Analysis Dashboard", layout="wide")

st.title("Urban Analysis Dashboard")

# Define file paths for datasets
data_files = {
    "Local Climate Zones (LCZ)": "data/LCZ.GeoJson.geojson",
    "Land Use": "data/Land_Use.geojson",
    "Vegetation Distribution (NDVI)": "data/NDVI-DS.geojson",
    "Roads": "data/Roads.geojson",
    "Urban Density": "data/UrbanDensity.geojson",
}

# Sidebar Controls
st.sidebar.title("Dashboard Controls")

# Filtering options for Roads
road_types = ["All", "Main Roads", "Secondary Roads"]
selected_road_type = st.sidebar.selectbox("Filter Roads by Type:", road_types)

# Filtering options for Urban Density
density_levels = ["All", "Low Density", "Medium Density", "High Density"]
selected_density = st.sidebar.selectbox("Filter Urban Density:", density_levels)

# Filtering options for Vegetation
timeframes = ["All Time", "Last Year", "Last 5 Years"]
selected_timeframe = st.sidebar.radio("Vegetation Data Timeframe:", timeframes)

# Add a button for filtering
apply_filter = st.sidebar.button("Apply Filters")

# Initialize a Folium map
map_center = [35.0, 44.0]  # Adjust to your region of interest
m = folium.Map(location=map_center, zoom_start=12, control_scale=True)

# Helper function to filter GeoDataFrame
def filter_gdf(gdf, column, value):
    if value == "All":
        return gdf
    return gdf[gdf[column] == value]

# Add layers with filtering
for name, path in data_files.items():
    gdf = gpd.read_file(path)
    
    # Apply specific filters
    if name == "Roads" and selected_road_type != "All":
        gdf = filter_gdf(gdf, "road_type", selected_road_type)
    elif name == "Urban Density" and selected_density != "All":
        gdf = filter_gdf(gdf, "density_level", selected_density)
    elif name == "Vegetation Distribution (NDVI)" and selected_timeframe != "All Time":
        # Add specific filtering logic for NDVI based on timeframes
        gdf = gdf[gdf["timeframe"] == selected_timeframe]
    
    # Ensure valid tooltips
    if len(gdf.columns) >= 2:
        fields = list(gdf.columns[:2])
        aliases = list(gdf.columns[:2])
    else:
        fields = []
        aliases = []

    # Add GeoJSON layer
    layer = folium.GeoJson(
        gdf,
        name=name,
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases) if fields else None
    )
    layer.add_to(m)

# Add layer control for toggling layers
folium.LayerControl().add_to(m)

# Display the map
st.subheader("Interactive Map with Layer Toggles and Filters")
st_data = st_folium(m, width=900, height=600)

# Sidebar Information
st.sidebar.write("### Hover Information")
st.sidebar.write(
    """
    Hover over points on the map to view detailed information about land use types, 
    population density, and more.
    """
)

st.sidebar.write("### Dynamic Updates")
st.sidebar.write(
    """
    Use the filters above to dynamically update the map based on road types, urban density, 
    or recent vegetation data.
    """
)







