import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Load the GeoJSON file
gdf = gpd.read_file('data/UrbanDensity.geojson')

# Check the data to make sure it's loaded correctly
st.write(gdf)

# Create a folium map centered around the GeoJSON data
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=12)

# Add the GeoJSON data to the map
folium.GeoJson(gdf).add_to(m)

# Render the map in Streamlit
st_folium(m, width=700)






































