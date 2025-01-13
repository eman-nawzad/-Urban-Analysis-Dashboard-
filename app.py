import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Load GeoJSON data
@st.cache_data
def load_data():
    try:
        ndvi_data = gpd.read_file('data/NDVIt.geojson')
        lcz_data = gpd.read_file('data/LCZ.GeoJson.geojson')
        urban_density_data = gpd.read_file('data/UrbanDensity.geojson')
        road_data = gpd.read_file('data/Roads.geojson')
        land_cover_data = gpd.read_file('data/Land_Use.geojson')
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None

    return ndvi_data, lcz_data, urban_density_data, road_data, land_cover_data

ndvi_data, lcz_data, urban_density_data, road_data, land_cover_data = load_data()

# Check if any data failed to load or is empty
if any(data is None or data.empty for data in [ndvi_data, lcz_data, urban_density_data, road_data, land_cover_data]):
    st.error("One or more datasets failed to load or are empty. Please check the files.")
    st.stop()

# Sidebar for layer selection
st.sidebar.header("Layer Selection")
selected_layers = st.sidebar.multiselect(
    "Select layers to display on the map:",
    ["NDVI", "LCZ", "Urban Density", "Roads", "Land Cover"],
    default=["NDVI", "LCZ", "Urban Density"]
)

# Create a folium map
m = folium.Map(location=[36.19, 44.01], zoom_start=12)

# Function to add layers to the map
def add_layer(data, layer_name, color, tooltip_column):
    for _, row in data.iterrows():
        if row.geometry.is_empty:
            continue
        coords = row.geometry.centroid.coords[0]
        folium.CircleMarker(
            location=[coords[1], coords[0]],
            radius=5,
            color=color,
            fill=True,
            fill_opacity=0.7,
            popup=f"{layer_name}: {row[tooltip_column]}",
            tooltip=row[tooltip_column],
        ).add_to(m)

# Add selected layers
if "NDVI" in selected_layers:
    filtered_ndvi = ndvi_data[ndvi_data['ndvi_class'].isin(["Dense Forest", "Sparse Grass"])]
    add_layer(filtered_ndvi, "NDVI", "green", "ndvi_class")

if "LCZ" in selected_layers:
    filtered_lcz = lcz_data[lcz_data['lcz_class'].isin(["Compact High-Rise", "Open Low-Rise", "Industrial Zones"])]
    add_layer(filtered_lcz, "LCZ", "blue", "lcz_class")

if "Urban Density" in selected_layers:
    filtered_density = urban_density_data[urban_density_data['density_class'].isin(["high density", "medium density", "low density", "very low density"])]
    add_layer(filtered_density, "Urban Density", "orange", "density_class")

if "Roads" in selected_layers:
    filtered_roads = road_data[road_data['highway'].isin(["primary", "motorway", "trunk", "secondary", "main"])]
    add_layer(filtered_roads, "Roads", "red", "highway")

if "Land Cover" in selected_layers:
    filtered_land_cover = land_cover_data[land_cover_data['land_use'] == "urban"]
    add_layer(filtered_land_cover, "Land Cover", "purple", "land_use")

# Display the map
st_data = st_folium(m, width=800, height=600)

st.sidebar.write("Use the map to explore the data.")

























