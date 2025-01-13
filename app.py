import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Load the GeoJSON file (replace with the path to your actual GeoJSON file)
gdf = gpd.read_file('data/UrbanDensity.geojson')

# Check the data to ensure it's loaded correctly
st.write(gdf)

# Create a dictionary for density classes (you can customize this if needed)
density_classes = {
    "Very Low Density (<10%)": 1,
    "Low Density (10–30%)": 2,
    "Medium Density (30–70%)": 3,
    "High Density (>70%)": 4
}

# Dropdown to select the density class
selected_class = st.selectbox(
    "Select Urban Density Class to View",
    list(density_classes.keys())
)

# Filter the data based on the selected class
filtered_gdf = gdf[gdf['density_class'] == density_classes[selected_class]]

# Create a Folium map centered around the filtered data
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()],
               zoom_start=12)

# Add the filtered GeoJSON data to the map
folium.GeoJson(filtered_gdf).add_to(m)

# Show the map in Streamlit
st_folium(m, width=700, height=500)






































