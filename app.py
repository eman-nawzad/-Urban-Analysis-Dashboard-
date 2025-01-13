import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium

# Sidebar: Add options to select the timeframe
st.sidebar.title("Select Timeframe")

# Set the date range from 2018 to 2023
start_date = '2018-01-01'
end_date = '2023-12-31'

# Display the selected date range in the sidebar
st.sidebar.write(f"Data from: {start_date} to {end_date}")

# Load your NDVI data (GeoJSON format in the repository)
ndvi_data_path = 'data/NDVIt.geojson'  # Path to your NDVI GeoJSON file
land_use_data_path = 'data/Land_Use.geojson'  # Path to your Land Use GeoJSON file
roads_data_path = 'data/Roads.geojson'  # Path to your Roads GeoJSON file
urban_density_data_path = 'data/UrbanDensity.geojson'  # Path to your Urban Density GeoJSON file

# Load GeoJSON files using GeoPandas
gdf_ndvi = gpd.read_file(ndvi_data_path)
gdf_land_use = gpd.read_file(land_use_data_path)
gdf_roads = gpd.read_file(roads_data_path)
gdf_urban_density = gpd.read_file(urban_density_data_path)

# Ensure all geometries are in the correct projection (EPSG:4326 for consistency with Leaflet)
gdf_ndvi = gdf_ndvi.to_crs(epsg=4326)
gdf_land_use = gdf_land_use.to_crs(epsg=4326)
gdf_roads = gdf_roads.to_crs(epsg=4326)
gdf_urban_density = gdf_urban_density.to_crs(epsg=4326)

# Sidebar: Allow users to toggle layers
toggle_ndvi = st.sidebar.checkbox("Show NDVI Layer", value=True)
toggle_land_use = st.sidebar.checkbox("Show Land Use Layer", value=False)
toggle_roads = st.sidebar.checkbox("Show Roads Layer", value=False)
toggle_urban_density = st.sidebar.checkbox("Show Urban Density Layer", value=False)

# Create a Folium map centered on the average location of the data
map_center = [gdf_ndvi.geometry.centroid.y.mean(), gdf_ndvi.geometry.centroid.x.mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Add layers based on user toggles
if toggle_ndvi:
    folium.GeoJson(
        gdf_ndvi.to_json(),
        name="NDVI Data",
        style_function=lambda x: {
            'fillColor': '#ff7800',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7
        }
    ).add_to(m)

if toggle_land_use:
    folium.GeoJson(
        gdf_land_use.to_json(),
        name="Land Use Data",
        style_function=lambda x: {
            'fillColor': 'green',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7
        }
    ).add_to(m)

if toggle_roads:
    folium.GeoJson(
        gdf_roads.to_json(),
        name="Roads Data",
        style_function=lambda x: {
            'color': 'blue',
            'weight': 2,
            'opacity': 0.7
        }
    ).add_to(m)

if toggle_urban_density:
    folium.GeoJson(
        gdf_urban_density.to_json(),
        name="Urban Density Data",
        style_function=lambda x: {
            'fillColor': 'purple',
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.5
        }
    ).add_to(m)

# Add layer control (toggle layers)
folium.LayerControl().add_to(m)

# Display the map in the Streamlit app
st_data = st_folium(m, width=900, height=600)














