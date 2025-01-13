import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Set Streamlit page configuration
st.set_page_config(page_title="Urban Analysis Dashboard", layout="wide")

st.title("Urban Analysis Dashboard")

# Define file paths
data_files = {
    "Local Climate Zones (LCZ)": "data/LCZ.GeoJson.geojson",
    "Land Use": "data/Land_Use.geojson",
    "NDVI Dataset": "data/NDVI-DS.geojson",
    "Roads": "data/Roads.geojson",
    "Urban Density": "data/UrbanDensity.geojson",
}

# Sidebar for selecting datasets
selected_file = st.sidebar.selectbox(
    "Select a dataset to view:",
    list(data_files.keys())
)

# Load the selected GeoJSON file
geojson_path = data_files[selected_file]
gdf = gpd.read_file(geojson_path)

# Display map
st.subheader(f"Map View: {selected_file}")
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()],
               zoom_start=12, control_scale=True)
folium.GeoJson(gdf).add_to(m)
st_data = st_folium(m, width=700, height=500)

# Display GeoJSON file data table
st.subheader(f"Data Table: {selected_file}")
st.dataframe(gdf)

st.write("Urban analysis is critical for understanding spatial patterns and planning sustainable cities.")






