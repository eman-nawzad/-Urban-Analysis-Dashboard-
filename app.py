import folium
import geopandas as gpd
import streamlit as st
from folium import GeoJson

# Load GeoJSON files from the data folder
LCZ = gpd.read_file('data/LCZ.GeoJson.geojson')
Land_Use = gpd.read_file('data/Land_Use.geojson')
NDVI_DS = gpd.read_file('data/NDVI-DS.geojson')
Roads = gpd.read_file('data/Roads.geojson')
UrbanDensity = gpd.read_file('data/UrbanDensity.geojson')

# Create a base map
m = folium.Map(location=[LCZ.geometry.centroid.y.mean(), LCZ.geometry.centroid.x.mean()], zoom_start=12)

# Add GeoJSON layers to the map
folium.GeoJson(LCZ).add_to(m)
folium.GeoJson(Land_Use).add_to(m)
folium.GeoJson(NDVI_DS).add_to(m)
folium.GeoJson(Roads).add_to(m)
folium.GeoJson(UrbanDensity).add_to(m)

# Add a title and description
st.title("Urban Analysis Dashboard")
st.markdown("""
This dashboard provides insights into various urban parameters such as Local Climate Zones (LCZ), 
Land Use, NDVI, Roads, and Urban Density. Explore these datasets through the interactive map below.
""")

# Display the map
# Instead of using `folium_static`, we display the Folium map using `st.map()`
# Convert the map into HTML and render it directly
map_html = m._repr_html_()
st.markdown(map_html, unsafe_allow_html=True)
