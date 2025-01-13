import streamlit as st
import ee
import folium
from streamlit_folium import st_folium

# Initialize the Earth Engine API
ee.Initialize()

# Sidebar: Add options to select the timeframe
st.sidebar.title("Select Timeframe")

# Set the date range from 2018 to 2023
start_date = '2018-01-01'
end_date = '2023-12-31'

# Display the selected date range in the sidebar
st.sidebar.write(f"Data from: {start_date} to {end_date}")

# Load the MODIS Percent Tree Cover dataset
dataset = ee.ImageCollection('MODIS/006/MOD44B') \
                .select('Percent_Tree_Cover') \
                .filterDate(start_date, end_date) \
                .first()  # Get the first image in the time range

# Load your polygon asset
polygon = ee.FeatureCollection('projects/ee-emannawzad/assets/Assignment_Map-polygon')

# Clip the dataset to the polygon
clipped_image = dataset.clip(polygon)

# Define thresholds for Dense Forest and Sparse Grass
dense_forest = clipped_image.gte(3).And(clipped_image.lte(5))  # Dense Forest (3–5%)
sparse_grass = clipped_image.gte(0.5).And(clipped_image.lte(3))  # Sparse Grass (0.5–3%)

# Combine the two categories into one single layer
combined_layer = dense_forest.multiply(1).add(sparse_grass.multiply(2))

# Mask the image to keep only the valid regions
masked_layer = combined_layer.updateMask(combined_layer)

# Create a folium map centered on the polygon
m = folium.Map(location=[polygon.geometry().centroid().getInfo()['coordinates'][1], polygon.geometry().centroid().getInfo()['coordinates'][0]], zoom_start=10)

# Add layers to the map
folium.TileLayer('cartodb positron').add_to(m)
folium.raster_layers.ImageOverlay(
    image=dataset.getMapId(),
    bounds=[[polygon.geometry().centroid().getInfo()['coordinates'][1], polygon.geometry().centroid().getInfo()['coordinates'][0]]],
    opacity=0.6
).add_to(m)

# Add layers for dense forest and sparse grass
folium.raster_layers.ImageOverlay(
    image=dense_forest.getMapId()['tile_fetcher'].url_format,
    bounds=[[polygon.geometry().centroid().getInfo()['coordinates'][1], polygon.geometry().centroid().getInfo()['coordinates'][0]]],
    opacity=0.5,
    name="Dense Forest"
).add_to(m)

folium.raster_layers.ImageOverlay(
    image=sparse_grass.getMapId()['tile_fetcher'].url_format,
    bounds=[[polygon.geometry().centroid().getInfo()['coordinates'][1], polygon.geometry().centroid().getInfo()['coordinates'][0]]],
    opacity=0.5,
    name="Sparse Grass"
).add_to(m)

# Add the combined layer (dense forest and sparse grass)
folium.raster_layers.ImageOverlay(
    image=masked_layer.getMapId()['tile_fetcher'].url_format,
    bounds=[[polygon.geometry().centroid().getInfo()['coordinates'][1], polygon.geometry().centroid().getInfo()['coordinates'][0]]],
    opacity=0.6,
    name="Combined Layer"
).add_to(m)

# Display the map in Streamlit
st_data = st_folium(m, width=900, height=600)













