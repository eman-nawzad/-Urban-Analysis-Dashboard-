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

# Load your GeoJSON data (NDVI, Land Use, Roads, Urban Density)
ndvi_data_path = 'data/NDVIt.geojson'  # Path to your NDVI GeoJSON file
land_use_data_path = 'data/Land_Use.geojson'  # Path to your Land Use GeoJSON file
roads_data_path = 'data/Roads.geojson'  # Path to your Roads GeoJSON file
urban_density_data_path = 'data/UrbanDensity.geojson'  # Path to your Urban Density GeoJSON file

# Load the GeoJSON files using GeoPandas
gdf_ndvi = gpd.read_file(ndvi_data_path)
gdf_land_use = gpd.read_file(land_use_data_path)
gdf_roads = gpd.read_file(roads_data_path)
gdf_urban_density = gpd.read_file(urban_density_data_path)

# Ensure all geometries are in the correct projection (EPSG:4326 for consistency with Leaflet)
gdf_ndvi = gdf_ndvi.to_crs(epsg=4326)
gdf_land_use = gdf_land_use.to_crs(epsg=4326)
gdf_roads = gdf_roads.to_crs(epsg=4326)
gdf_urban_density = gdf_urban_density.to_crs(epsg=4326)

# Create a Folium map centered on the average location of the data
map_center = [gdf_ndvi.geometry.centroid.y.mean(), gdf_ndvi.geometry.centroid.x.mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Create GeoJSON layers for each dataset with custom styling
ndvi_layer = folium.GeoJson(
    gdf_ndvi.to_json(),
    name="NDVI Data",
    style_function=lambda x: {
        'fillColor': '#ff7800',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7
    }
)

land_use_layer = folium.GeoJson(
    gdf_land_use.to_json(),
    name="Land Use Data",
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.7
    }
)

roads_layer = folium.GeoJson(
    gdf_roads.to_json(),
    name="Roads Data",
    style_function=lambda x: {
        'color': 'blue',
        'weight': 2,
        'opacity': 0.7
    }
)

urban_density_layer = folium.GeoJson(
    gdf_urban_density.to_json(),
    name="Urban Density Data",
    style_function=lambda x: {
        'fillColor': 'purple',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5
    }
)

# Add the layers to the map
ndvi_layer.add_to(m)
land_use_layer.add_to(m)
roads_layer.add_to(m)
urban_density_layer.add_to(m)

# Add a Layer Control to the map for toggling visibility of all layers
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st_data = st_folium(m, width=900, height=600)




























