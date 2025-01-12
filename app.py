import folium
import geopandas as gpd
import streamlit as st
import os

# Load GeoJSON files from the data folder
LCZ = gpd.read_file('data/LCZ.GeoJson.geojson')
Land_Use = gpd.read_file('data/Land_Use.geojson')
NDVI_DS = gpd.read_file('data/NDVI-DS.geojson')
Roads = gpd.read_file('data/Roads.geojson')
UrbanDensity = gpd.read_file('data/UrbanDensity.geojson')

# Create a base map centered around the first GeoJSON layer's centroid
m = folium.Map(location=[LCZ.geometry.centroid.y.mean(), LCZ.geometry.centroid.x.mean()], zoom_start=12)

# Create FeatureGroups for each GeoJSON layer
lcz_group = folium.FeatureGroup(name="LCZ")
land_use_group = folium.FeatureGroup(name="Land Use")
ndvi_ds_group = folium.FeatureGroup(name="NDVI-DS")
roads_group = folium.FeatureGroup(name="Roads")
urban_density_group = folium.FeatureGroup(name="Urban Density")

# Add GeoJSON layers to the respective FeatureGroups
folium.GeoJson(LCZ).add_to(lcz_group)
folium.GeoJson(Land_Use).add_to(land_use_group)
folium.GeoJson(NDVI_DS).add_to(ndvi_ds_group)
folium.GeoJson(Roads).add_to(roads_group)
folium.GeoJson(UrbanDensity).add_to(urban_density_group)

# Add FeatureGroups to the map
lcz_group.add_to(m)
land_use_group.add_to(m)
ndvi_ds_group.add_to(m)
roads_group.add_to(m)
urban_density_group.add_to(m)

# Add LayerControl to allow toggling between layers
folium.LayerControl().add_to(m)

# Add a title and description to the Streamlit app
st.title("Urban Analysis Dashboard")
st.markdown("""
This dashboard provides insights into various urban parameters such as Local Climate Zones (LCZ), 
Land Use, NDVI, Roads, and Urban Density. Explore these datasets through the interactive map below.
""")

# Save the map to an HTML file
map_file = "temp_map_with_layers.html"
m.save(map_file)

# Use Streamlit's HTML component to render the map
st.components.v1.html(open(map_file, 'r').read(), height=500)

# Clean up the temporary file
os.remove(map_file)


