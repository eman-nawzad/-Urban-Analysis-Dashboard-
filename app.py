import streamlit as st
import folium
from folium import GeoJson
from streamlit_folium import st_folium
import json

# Load GeoJSON data
@st.cache_data
def load_geojson(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load all GeoJSON files
ndvi_data = load_geojson('data/NDVIt.geojson')
lcz_data = load_geojson('data/LCZ.GeoJson.geojson')
urban_density_data = load_geojson('data/UrbanDensity.geojson')
road_data = load_geojson('data/Roads.geojson')
land_cover_data = load_geojson('data/Land_Use.geojson')

# Sidebar configuration
st.sidebar.header("Map Filters")

# Layer options
layer_options = ["NDVI", "LCZ", "Urban Density", "Roads", "Land Cover"]
selected_layers = st.sidebar.multiselect("Select layers to display:", layer_options, default=layer_options)

# Filter options for each layer
filters = {
    "NDVI": ["Dense Forest", "Sparse Grass"],
    "LCZ": ["Compact High-Rise", "Open Low-Rise", "Industrial Zones"],
    "Urban Density": ["High Density", "Medium Density", "Low Density", "Very Low Density"],
    "Roads": ["Primary", "Motorway", "Trunk", "Secondary", "Main"],
    "Land Cover": ["Urban"]
}

selected_filters = {}
for layer in selected_layers:
    selected_filters[layer] = st.sidebar.multiselect(f"Select {layer} categories:", filters[layer], default=filters[layer])

# Create a Folium map
m = folium.Map(location=[36.2, 44.0], zoom_start=10)

# Add layers based on user selection
if "NDVI" in selected_layers:
    filtered_ndvi = {
        "type": "FeatureCollection",
        "features": [f for f in ndvi_data["features"] if f["properties"]["category"] in selected_filters["NDVI"]]
    }
    GeoJson(filtered_ndvi, name="NDVI", style_function=lambda x: {
        'color': 'green',
        'weight': 2
    }).add_to(m)

if "LCZ" in selected_layers:
    filtered_lcz = {
        "type": "FeatureCollection",
        "features": [f for f in lcz_data["features"] if f["properties"]["category"] in selected_filters["LCZ"]]
    }
    GeoJson(filtered_lcz, name="LCZ", style_function=lambda x: {
        'color': 'blue',
        'weight': 2
    }).add_to(m)

if "Urban Density" in selected_layers:
    filtered_density = {
        "type": "FeatureCollection",
        "features": [f for f in urban_density_data["features"] if f["properties"]["category"] in selected_filters["Urban Density"]]
    }
    GeoJson(filtered_density, name="Urban Density", style_function=lambda x: {
        'color': 'purple',
        'weight': 2
    }).add_to(m)

if "Roads" in selected_layers:
    filtered_roads = {
        "type": "FeatureCollection",
        "features": [f for f in road_data["features"] if f["properties"]["highway"] in selected_filters["Roads"]]
    }
    GeoJson(filtered_roads, name="Roads", style_function=lambda x: {
        'color': 'red',
        'weight': 1
    }).add_to(m)

if "Land Cover" in selected_layers:
    filtered_land_cover = {
        "type": "FeatureCollection",
        "features": [f for f in land_cover_data["features"] if f["properties"]["land_use"] in selected_filters["Land Cover"]]
    }
    GeoJson(filtered_land_cover, name="Land Cover", style_function=lambda x: {
        'color': 'orange',
        'weight': 2
    }).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st.title("Interactive Map with Filters")
st_folium(m, width=700, height=500)



























