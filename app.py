import streamlit as st
import folium
from folium import plugins
from streamlit_folium import st_folium
import geopandas as gpd

# Load the GeoJSON files
lcz = gpd.read_file('data/LCZ.GeoJson.geojson')
land_use = gpd.read_file('data/Land_Use.geojson')
ndvi = gpd.read_file('data/NDVIt.geojson')
roads = gpd.read_file('data/Roads.geojson')
urban_density = gpd.read_file('data/UrbanDensity.geojson')

# Create a folium map centered on a specific location
m = folium.Map(location=[39.5, 46.0], zoom_start=12)

# Define custom colors for each layer
color_palettes = {
    "Land Use": {'Residential': 'lightblue', 'Commercial': 'lightyellow', 'Industrial': 'lightgray'},
    "Local Climate Zones (LCZ)": {'high-rise': 'red', 'low-rise': 'green', 'urban': 'purple'},
    "Vegetation (NDVI)": {'Dense Forest': 'darkgreen', 'Sparse Grass': 'lightgreen'},
    "Roads": {'Main Roads': 'blue', 'Secondary Roads': 'orange'},
    "Urban Density": {'High': 'darkred', 'Low': 'lightred'}
}

# Add Land Use Layer
for idx, row in land_use.iterrows():
    folium.GeoJson(
        row['geometry'],
        name="Land Use",
        style_function=lambda feature: {
            'fillColor': color_palettes["Land Use"].get(row['land_use_type'], 'gray'),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        }
    ).add_to(m)

# Add Local Climate Zones (LCZ) Layer
for idx, row in lcz.iterrows():
    folium.GeoJson(
        row['geometry'],
        name="LCZ",
        style_function=lambda feature: {
            'fillColor': color_palettes["Local Climate Zones (LCZ)"].get(row['lcz_type'], 'gray'),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        }
    ).add_to(m)

# Add Vegetation (NDVI) Layer
for idx, row in ndvi.iterrows():
    folium.GeoJson(
        row['geometry'],
        name="Vegetation (NDVI)",
        style_function=lambda feature: {
            'fillColor': color_palettes["Vegetation (NDVI)"].get(row['vegetation_type'], 'gray'),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        }
    ).add_to(m)

# Add Roads Layer
for idx, row in roads.iterrows():
    folium.GeoJson(
        row['geometry'],
        name="Roads",
        style_function=lambda feature: {
            'color': color_palettes["Roads"].get(row['road_type'], 'gray'),
            'weight': 3,
            'opacity': 0.8
        }
    ).add_to(m)

# Add Urban Density Layer
for idx, row in urban_density.iterrows():
    folium.GeoJson(
        row['geometry'],
        name="Urban Density",
        style_function=lambda feature: {
            'fillColor': color_palettes["Urban Density"].get(row['density_level'], 'gray'),
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6
        }
    ).add_to(m)

# Add Layer Control
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st_data = st_folium(m, width=900, height=600)






























