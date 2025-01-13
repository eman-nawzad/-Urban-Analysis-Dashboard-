import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium

# Sidebar: Add options to select the layer
st.sidebar.title("Select Layer")

# Create a dropdown menu in the sidebar to select the layer
layer_options = ['None', 'NDVI Data', 'Land Use Data', 'Roads Data', 'Urban Density Data']
selected_layer = st.sidebar.selectbox('Choose a layer to display:', layer_options)

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

# Define the layers for each dataset
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

# Add selected layer based on user's choice
if selected_layer == 'NDVI Data':
    ndvi_layer.add_to(m)
elif selected_layer == 'Land Use Data':
    land_use_layer.add_to(m)
elif selected_layer == 'Roads Data':
    roads_layer.add_to(m)
elif selected_layer == 'Urban Density Data':
    urban_density_layer.add_to(m)

# Add a Layer Control to the map for toggling visibility of the selected layer
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st_data = st_folium(m, width=900, height=600)





























