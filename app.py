import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Load the GeoJSON file
gdf = gpd.read_file('data/UrbanDensity.geojson')

# Check the columns in the GeoDataFrame to find the correct density class column
st.write(gdf.columns)

# Create a dictionary for density classes
density_classes = {
    "Very Low Density (<10%)": 1,
    "Low Density (10–30%)": 2,
    "Medium Density (30–70%)": 3,
    "High Density (>70%)": 4
}

# Sidebar for selecting multiple density classes
st.sidebar.title("Select Urban Density Classes")
selected_classes = st.sidebar.multiselect(
    "Choose Urban Density Classes to View",
    list(density_classes.keys())
)

# Filter the data based on selected classes
if selected_classes:
    selected_class_values = [density_classes[cls] for cls in selected_classes]
    filtered_gdf = gdf[gdf['density_class'].isin(selected_class_values)]
else:
    filtered_gdf = gdf  # If no class selected, show all data

# Create a Folium map centered around the filtered data
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()],
               zoom_start=12)

# Add the filtered GeoJSON data to the map
folium.GeoJson(filtered_gdf).add_to(m)

# Show the map in Streamlit
st_folium(m, width=700, height=500)










































