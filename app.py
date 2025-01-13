import streamlit as st
import folium
import geopandas as gpd
from folium import plugins
from streamlit_folium import st_folium

# Load GeoJSON data
land_use_data = gpd.read_file("path_to_land_use.geojson")
lcz_data = gpd.read_file("path_to_lcz.geojson")
ndvi_data = gpd.read_file("path_to_ndvi.geojson")
road_data = gpd.read_file("path_to_roads.geojson")
urban_density_data = gpd.read_file("path_to_urban_density.geojson")

# Define custom colors for each layer
color_palettes = {
    "Land Use": {
        'Residential': 'lightblue', 
        'Commercial': 'lightyellow', 
        'Industrial': 'lightgray'
    },
    "Local Climate Zones (LCZ)": {
        'Compact High-Rise': 'red', 
        'Open Low-Rise': 'green', 
        'Industrial Zones': 'purple'
    },
    "Vegetation (NDVI)": {
        'Dense Forest': 'darkgreen', 
        'Sparse Grass': 'lightgreen'
    },
    "Roads": {
        'primary': 'blue', 
        'motorway': 'green', 
        'trunk': 'orange', 
        'secondary': 'red',
        'main': 'purple'
    },
    "Urban Density": {
        'High': 'darkred', 
        'Medium': 'orange', 
        'Low': 'lightgreen', 
        'Very Low': 'lightblue'
    }
}

# Function to style layers based on custom colors
def style_function(feature, layer_type):
    try:
        # Try to get the value from feature properties
        property_value = feature['properties'].get(layer_type, None)
        if property_value:
            # Apply the color based on the property value
            return {
                'fillColor': color_palettes[layer_type].get(property_value, 'gray'),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
        else:
            # Default color if the property value is missing
            return {
                'fillColor': 'gray',  # Default color
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
    except KeyError:
        # Handle any unexpected errors
        return {
            'fillColor': 'gray',  # Default color for unknown properties
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        }

# Initialize map
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Add selected layers to the map
selected_layers = ['Land Use', 'Local Climate Zones (LCZ)', 'Vegetation (NDVI)', 'Roads', 'Urban Density']

if "Land Use" in selected_layers:
    folium.GeoJson(
        land_use_data,
        style_function=lambda feature: style_function(feature, "Land Use")
    ).add_to(m)

if "Local Climate Zones (LCZ)" in selected_layers:
    folium.GeoJson(
        lcz_data,
        style_function=lambda feature: style_function(feature, "Local Climate Zones (LCZ)")
    ).add_to(m)

if "Vegetation (NDVI)" in selected_layers:
    folium.GeoJson(
        ndvi_data,
        style_function=lambda feature: style_function(feature, "Vegetation (NDVI)")
    ).add_to(m)

if "Roads" in selected_layers:
    folium.GeoJson(
        road_data,
        style_function=lambda feature: style_function(feature, "Roads")
    ).add_to(m)

if "Urban Density" in selected_layers:
    folium.GeoJson(
        urban_density_data,
        style_function=lambda feature: style_function(feature, "Urban Density")
    ).add_to(m)

# Display map in Streamlit
st_folium(m, width=700, height=500)




















