import streamlit as st
import geopandas as gpd
import folium
from folium import plugins
from streamlit_folium import st_folium

import os

file_path = 'data/UrbanDensity.geojson'
if os.path.exists(file_path):
    gdf = gpd.read_file(file_path)
else:
    st.error(f"File {file_path} not found!")


# Create a dropdown selector in Streamlit for filtering the density classes
density_classes = {
    "Very Low Density (<10%)": 1,
    "Low Density (10–30%)": 2,
    "Medium Density (30–70%)": 3,
    "High Density (>70%)": 4
}

# Dropdown to choose density class
selected_class = st.selectbox(
    "Select Urban Density Class to View",
    list(density_classes.keys())
)

# Filter the data based on user selection
filtered_gdf = gdf[gdf['density_class'] == density_classes[selected_class]]

# Create a Folium map to display the filtered data
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()],
               zoom_start=12)

# Add filtered data as GeoJSON on the map
folium.GeoJson(filtered_gdf).add_to(m)

# Show the map in Streamlit
st_folium(m, width=700, height=500)





































