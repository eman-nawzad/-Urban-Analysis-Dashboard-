import streamlit as st
import folium
from folium import plugins
import geopandas as gpd

# Load GeoJSON data
lcz = gpd.read_file('data/LCZ.GeoJson.geojson')
land_use = gpd.read_file('data/Land_Use.geojson')
ndvi = gpd.read_file('data/NDVI-DS.geojson')
roads = gpd.read_file('data/Roads.geojson')
urban_density = gpd.read_file('data/UrbanDensity.geojson')

# Create a base map
m = folium.Map(location=[35.5, 45.5], zoom_start=10)

# Add Land Use Layer
land_use_layer = folium.FeatureGroup(name='Land Use').add_to(m)
folium.GeoJson(land_use, style_function=lambda x: {
    'fillColor': 'green' if x['properties']['type'] == 'residential' else 'red',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.5
}).add_to(land_use_layer)

# Add Local Climate Zones Layer
lcz_layer = folium.FeatureGroup(name='Local Climate Zones').add_to(m)
folium.GeoJson(lcz, style_function=lambda x: {
    'fillColor': 'blue' if x['properties']['zone'] == 'high-rise' else 'yellow',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.5
}).add_to(lcz_layer)

# Add Vegetation Distribution Layer
ndvi_layer = folium.FeatureGroup(name='Vegetation Distribution').add_to(m)
folium.GeoJson(ndvi, style_function=lambda x: {
    'fillColor': 'green' if x['properties']['vegetation'] == 'dense forest' else 'lightgreen',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.5
}).add_to(ndvi_layer)

# Add Roads Layer
roads_layer = folium.FeatureGroup(name='Roads').add_to(m)
folium.GeoJson(roads, style_function=lambda x: {
    'color': 'red' if x['properties']['type'] == 'main' else 'orange',
    'weight': 2
}).add_to(roads_layer)

# Add Urban Density Layer
urban_density_layer = folium.FeatureGroup(name='Urban Density').add_to(m)
folium.GeoJson(urban_density, style_function=lambda x: {
    'fillColor': 'purple' if x['properties']['density'] == 'high' else 'lightpurple',
    'color': 'black',
    'weight': 1,
    'fillOpacity': 0.5
}).add_to(urban_density_layer)

# Add Layer Control
folium.LayerControl().add_to(m)

# Display map using Streamlit
st.title("Urban Analysis Dashboard")
st.map(m._repr_html_(), use_container_width=True)

