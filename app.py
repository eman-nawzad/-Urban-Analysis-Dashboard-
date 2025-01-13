import streamlit as st
import folium
import geopandas as gpd
from streamlit_folium import st_folium
import pandas as pd

# Sidebar: Interactive Filters for Layers
st.sidebar.title("Map Filters")

# Select filter options for roads, land use, and urban density
road_types = ['All', 'Primary', 'Secondary', 'Tertiary']
selected_road_type = st.sidebar.selectbox('Select Road Type:', road_types)

land_use_types = ['All', 'Residential', 'Commercial', 'Industrial', 'Agricultural']
selected_land_use_type = st.sidebar.selectbox('Select Land Use Type:', land_use_types)

urban_density_range = st.sidebar.slider("Select Urban Density Range", 0, 100, (0, 100))
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-12-31"))

# Load the GeoJSON data
ndvi_data_path = 'data/NDVIt.geojson'
land_use_data_path = 'data/Land_Use.geojson'
roads_data_path = 'data/Roads.geojson'
urban_density_data_path = 'data/UrbanDensity.geojson'

gdf_ndvi = gpd.read_file(ndvi_data_path)
gdf_land_use = gpd.read_file(land_use_data_path)
gdf_roads = gpd.read_file(roads_data_path)
gdf_urban_density = gpd.read_file(urban_density_data_path)

# Filter NDVI data based on selected dates
gdf_ndvi['date'] = pd.to_datetime(gdf_ndvi['date'])
gdf_ndvi_filtered = gdf_ndvi[(gdf_ndvi['date'] >= start_date) & (gdf_ndvi['date'] <= end_date)]

# Filter roads by type
if selected_road_type != 'All':
    gdf_roads = gdf_roads[gdf_roads['highway'] == selected_road_type]

# Filter land use by type
if selected_land_use_type != 'All':
    gdf_land_use = gdf_land_use[gdf_land_use['land_use_type'] == selected_land_use_type]

# Filter urban density by range
gdf_urban_density = gdf_urban_density[
    (gdf_urban_density['density'] >= urban_density_range[0]) & 
    (gdf_urban_density['density'] <= urban_density_range[1])
]

# Ensure all geometries are in the correct projection (EPSG:4326)
gdf_ndvi = gdf_ndvi.to_crs(epsg=4326)
gdf_land_use = gdf_land_use.to_crs(epsg=4326)
gdf_roads = gdf_roads.to_crs(epsg=4326)
gdf_urban_density = gdf_urban_density.to_crs(epsg=4326)
gdf_ndvi_filtered = gdf_ndvi_filtered.to_crs(epsg=4326)

# Create a Folium map centered on the filtered data
map_center = [gdf_ndvi_filtered.geometry.centroid.y.mean(), gdf_ndvi_filtered.geometry.centroid.x.mean()]
m = folium.Map(location=map_center, zoom_start=10)

# Define the layers for each dataset with hover info
ndvi_layer = folium.GeoJson(
    gdf_ndvi_filtered.to_json(),
    name="NDVI Data",
    tooltip=folium.GeoJsonTooltip(fields=['ndvi_value']),
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
    tooltip=folium.GeoJsonTooltip(fields=['land_use_type']),
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
    tooltip=folium.GeoJsonTooltip(fields=['highway']),
    style_function=lambda x: {
        'color': 'blue',
        'weight': 2,
        'opacity': 0.7
    }
)

urban_density_layer = folium.GeoJson(
    gdf_urban_density.to_json(),
    name="Urban Density Data",
    tooltip=folium.GeoJsonTooltip(fields=['density']),
    style_function=lambda x: {
        'fillColor': 'purple',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5
    }
)

# Add the selected layer(s) to the map
if selected_road_type == 'All':
    ndvi_layer.add_to(m)
    land_use_layer.add_to(m)
    roads_layer.add_to(m)
    urban_density_layer.add_to(m)
else:
    roads_layer.add_to(m)

# Add a Layer Control to the map for toggling visibility of the layers
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st_folium(m, width=900, height=600)


































