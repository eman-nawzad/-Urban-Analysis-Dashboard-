import folium
import streamlit as st
import geopandas as gpd
import pandas as pd
from folium import plugins

# Read GeoJSON files from the repository
land_use_data = gpd.read_file("data/Land_Use.geojson")
lcz_data = gpd.read_file("data/LCZ.GeoJson.geojson")
ndvi_data = gpd.read_file("data/NDVIt.geojson")
roads_data = gpd.read_file("data/Roads.geojson")
urban_density_data = gpd.read_file("data/UrbanDensity.geojson")

# Define custom colors for each layer
color_palettes = {
    "Land Use": {'Residential': 'lightblue', 'Commercial': 'lightyellow', 'Industrial': 'lightgray'},
    "Local Climate Zones (LCZ)": {'Compact High-Rise': 'blue', 'Open Low-Rise': 'orange', 'Industrial Zones': 'red'},
    "Vegetation (NDVI)": {'Dense Forest': 'darkgreen', 'Sparse Grass': 'lightgreen'},
    "Roads": {'Primary': 'blue', 'Motorway': 'red', 'Trunk': 'green', 'Secondary': 'orange', 'Main': 'yellow'},
    "Urban Density": {'High Density': 'darkred', 'Medium Density': 'red', 'Low Density': 'orange', 'Very Low Density': 'lightyellow'}
}

# Initialize the map
m = folium.Map(location=[35.6895, 139.6917], zoom_start=12)

# Sidebar for Layer Control
st.sidebar.title("Layer Control")
layer_options = [
    "Land Use",
    "Local Climate Zones (LCZ)",
    "Vegetation (NDVI)",
    "Roads",
    "Urban Density"
]

selected_layers = st.sidebar.multiselect("Select layers to display", layer_options, default=layer_options)

# Function to style layers based on custom colors
def style_function(feature, layer_type):
    return {
        'fillColor': color_palettes[layer_type].get(feature['properties'][layer_type], 'gray'),
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.7
    }

# Add selected layers to the map
if "Land Use" in selected_layers:
    folium.GeoJson(
        land_use_data,
        style_function=lambda feature: style_function(feature, "Land Use")
    ).add_to(m)

if "Local Climate Zones (LCZ)" in selected_layers:
    folium.GeoJson(
        lcz_data,
        style_function=lambda feature: style_function(feature, "LCZ")
    ).add_to(m)

if "Vegetation (NDVI)" in selected_layers:
    folium.GeoJson(
        ndvi_data,
        style_function=lambda feature: style_function(feature, "Vegetation (NDVI)")
    ).add_to(m)

if "Roads" in selected_layers:
    folium.GeoJson(
        roads_data,
        style_function=lambda feature: style_function(feature, "Roads")
    ).add_to(m)

if "Urban Density" in selected_layers:
    folium.GeoJson(
        urban_density_data,
        style_function=lambda feature: style_function(feature, "Urban Density")
    ).add_to(m)

# Add Layer Control
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st.title("Urban Analysis Dashboard")
st.write("This is your Urban Analysis Dashboard with interactive layers.")

# Show the map in Streamlit
st_data = m._repr_html_()
st.markdown(st_data, unsafe_allow_html=True)



















