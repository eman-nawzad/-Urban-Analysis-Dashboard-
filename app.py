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

# Initialize a Folium map
map_center = [35.0, 44.0]  # Adjust to your region of interest
m = folium.Map(location=map_center, zoom_start=12, control_scale=True)

# Add layers to the map with tooltips
for name, path in data_files.items():
    gdf = gpd.read_file(path)
    
    # Ensure at least two columns exist for tooltips
    if len(gdf.columns) >= 2:
        fields = list(gdf.columns[:2])  # Convert to a list
        aliases = list(gdf.columns[:2])  # Set aliases
    else:
        fields = []  # No fields available
        aliases = []

    # Add GeoJSON layer to the map
    layer = folium.GeoJson(
        gdf,
        name=name,
        tooltip=folium.GeoJsonTooltip(fields=fields, aliases=aliases) if fields else None
    )
    layer.add_to(m)

# Add layer control for toggling layers
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st.subheader("Interactive Map with Layer Toggles")
st_data = st_folium(m, width=900, height=600)

st.write(
    """
    Use the interactive map above to toggle layers for land use, local climate zones, 
    vegetation distribution, roads, and urban density.
    """
)







