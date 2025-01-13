import streamlit as st
import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import box

# Load GeoJSON data
@st.cache_data
def load_geojson(file_path):
    try:
        return gpd.read_file(file_path)
    except Exception as e:
        st.error(f"Error loading {file_path}: {e}")
        return None

# Load all GeoJSON files
ndvi_data = load_geojson('data/NDVIt.geojson')
lcz_data = load_geojson('data/LCZ.GeoJson.geojson')
urban_density_data = load_geojson('data/UrbanDensity.geojson')
road_data = load_geojson('data/Roads.geojson')
land_cover_data = load_geojson('data/Land_Use.geojson')

# Check if data is loaded
if not all([ndvi_data, lcz_data, urban_density_data, road_data, land_cover_data]):
    st.error("Failed to load one or more GeoJSON files. Check file paths or format.")
    st.stop()

# Sidebar configuration
st.sidebar.header("Map Filters")

# Layer options
layer_options = ["NDVI", "LCZ", "Urban Density", "Roads", "Land Cover"]
selected_layers = st.sidebar.multiselect("Select layers to display:", layer_options, default=layer_options)

# Filter options for each layer
filters = {
    "NDVI": ["Dense Forest", "Sparse Grass"],
    "LCZ": ["Compact High-Rise", "Open Low-Rise", "Industrial Zones"],
    "Urban Density": ["High Density", "Medium Density", "Low Density", "Very Low Density"],
    "Roads": ["Primary", "Motorway", "Trunk", "Secondary", "Main"],
    "Land Cover": ["Urban"]
}

selected_filters = {}
for layer in selected_layers:
    selected_filters[layer] = st.sidebar.multiselect(f"Select {layer} categories:", filters[layer], default=filters[layer])

# Create a base map
fig, ax = plt.subplots(figsize=(10, 10))
world_bounds = box(-180, -90, 180, 90)
world = gpd.GeoSeries([world_bounds]).set_crs(epsg=4326)
world.boundary.plot(ax=ax, color="black")

# Add layers based on user selection
if "NDVI" in selected_layers:
    filtered_ndvi = ndvi_data[ndvi_data["category"].isin(selected_filters["NDVI"])]
    filtered_ndvi.plot(ax=ax, color="green", label="NDVI")

if "LCZ" in selected_layers:
    filtered_lcz = lcz_data[lcz_data["category"].isin(selected_filters["LCZ"])]
    filtered_lcz.plot(ax=ax, color="blue", label="LCZ")

if "Urban Density" in selected_layers:
    filtered_density = urban_density_data[urban_density_data["category"].isin(selected_filters["Urban Density"])]
    filtered_density.plot(ax=ax, color="purple", label="Urban Density")

if "Roads" in selected_layers:
    filtered_roads = road_data[road_data["highway"].isin(selected_filters["Roads"])]
    filtered_roads.plot(ax=ax, color="red", label="Roads", linewidth=0.5)

if "Land Cover" in selected_layers:
    filtered_land_cover = land_cover_data[land_cover_data["land_use"].isin(selected_filters["Land Cover"])]
    filtered_land_cover.plot(ax=ax, color="orange", label="Land Cover")

# Finalize map
ax.legend()
ax.set_title("Interactive Map")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Display the map in Streamlit
st.pyplot(fig)




























