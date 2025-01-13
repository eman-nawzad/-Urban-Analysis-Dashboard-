import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import os

# Function to load GeoJSON data with error handling
@st.cache_data
def load_data(file_path, layer_name):
    if os.path.exists(file_path):
        try:
            data = gpd.read_file(file_path)
            return data
        except Exception as e:
            st.error(f"Failed to load {layer_name}: {e}")
            return None
    else:
        st.error(f"File not found: {file_path}")
        return None

# Load datasets
ndvi_data = load_data('data/NDVI-DS.geojson', 'NDVI')
lcz_data = load_data('data/LCZ.GeoJson.geojson', 'LCZ')
urban_density_data = load_data('data/UrbanDensity.geojson', 'Urban Density')
road_data = load_data('data/Roads.geojson', 'Roads')
land_cover_data = load_data('data/Land_Use.geojson', 'Land Cover')

# Check if data loaded successfully
if not all([ndvi_data, lcz_data, urban_density_data, road_data, land_cover_data]):
    st.stop()  # Stop the app if any dataset fails to load

# Sidebar for layer selection
st.sidebar.header("Layer Selection")
selected_layers = st.sidebar.multiselect(
    "Select layers to display on the map:",
    ["NDVI", "LCZ", "Urban Density", "Roads", "Land Cover"],
    default=["NDVI", "LCZ", "Urban Density"]
)

# Create a folium map
m = folium.Map(location=[36.19, 44.01], zoom_start=12)

# Function to add layers to the map
def add_layer(data, layer_name, color, tooltip_column):
    """Adds a layer to the folium map."""
    for _, row in data.iterrows():
        if row.geometry.geom_type == 'Point':
            coords = [row.geometry.y, row.geometry.x]
        else:
            coords = [row.geometry.centroid.y, row.geometry.centroid.x]
        
        folium.CircleMarker(
            location=coords,
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"{layer_name}: {row[tooltip_column]}",
            tooltip=row[tooltip_column],
        ).add_to(m)

# Add selected layers to the map
if "NDVI" in selected_layers:
    filtered_ndvi = ndvi_data[ndvi_data['ndvi_class'].isin(["Dense Forest", "Sparse Grass"])]
    add_layer(filtered_ndvi, "NDVI", "green", "ndvi_class")

if "LCZ" in selected_layers:
    filtered_lcz = lcz_data[lcz_data['lcz_class'].isin(["Compact High-Rise", "Open Low-Rise", "Industrial Zones"])]
    add_layer(filtered_lcz, "LCZ", "blue", "lcz_class")

if "Urban Density" in selected_layers:
    filtered_density = urban_density_data[urban_density_data['density_class'].isin(["high density", "medium density", "low density", "very low density"])]
    add_layer(filtered_density, "Urban Density", "orange", "density_class")

if "Roads" in selected_layers:
    filtered_roads = road_data[road_data['highway'].isin(["primary", "motorway", "trunk", "secondary",
























