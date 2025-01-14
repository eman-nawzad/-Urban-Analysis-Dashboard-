import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Define dataset paths
data_files = {
    "Urban Density": "data/UrbanDensity.geojson",
    "LCZ": "data/LCZ_Zones.geojson",
    "Land Use": "data/Land_Use.geojson",
    "NDVI": "data/NDVIm.geojson",
    "Roads": "data/Roads.geojson"
}

# Sidebar
st.sidebar.title("Dataset Viewer")
show_all_layers = st.sidebar.checkbox("Show All Layers")
selected_file = st.sidebar.selectbox("Choose a dataset", list(data_files.keys()))

# Load the selected dataset
gdf = gpd.read_file(data_files[selected_file])

# Filter the dataset based on user input
filtered_gdf = gdf.copy()
if selected_file == "Urban Density":
    density_classes = {
        "Very Low Density (<10%)": 1,
        "Low Density (10–30%)": 2,
        "Medium Density (30–70%)": 3,
        "High Density (>70%)": 4
    }
    density_filter = st.sidebar.selectbox(
        "Filter by Urban Density Class", ["All"] + list(density_classes.keys())
    )
    if density_filter != "All":
        class_value = density_classes[density_filter]
        filtered_gdf = gdf[gdf['label'] == class_value]

elif selected_file == "LCZ":
    lcz_classes = {"Compact High-Rise": 1, "Open Low-Rise": 6, "Industrial Zones": 8}
    lcz_filter = st.sidebar.selectbox("Filter by LCZ Class", ["All"] + list(lcz_classes.keys()))
    if lcz_filter != "All":
        class_value = lcz_classes[lcz_filter]
        filtered_gdf = gdf[gdf['LCZ_Filter'] == class_value]

elif selected_file == "Land Use":
    land_use_classes = {3: "Croplands", 4: "Urban", 6: "Barren"}
    land_use_filter = st.sidebar.selectbox(
        "Filter by Land Use Class", ["All"] + list(land_use_classes.values())
    )
    if land_use_filter != "All":
        class_value = [k for k, v in land_use_classes.items() if v == land_use_filter][0]
        filtered_gdf = gdf[gdf['land_use'] == class_value]

elif selected_file == "NDVI":
    if 'label' in gdf.columns:
        unique_labels = gdf['label'].unique()
        ndvi_filter = st.sidebar.selectbox("Filter by NDVI Class", ["All"] + list(unique_labels))
        if ndvi_filter != "All":
            filtered_gdf = gdf[gdf['label'] == ndvi_filter]

elif selected_file == "Roads":
    if 'highway' in gdf.columns:
        highway_types = gdf['highway'].unique()
        road_filter = st.sidebar.selectbox("Filter by Road Type", ["All"] + list(highway_types))
        if road_filter != "All":
            filtered_gdf = gdf[gdf['highway'] == road_filter]

# Sidebar warning message for no data
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected class in the '{selected_file}' dataset. Please try a different selection.")
else:
    st.sidebar.success(f"Displaying data from the '{selected_file}' dataset.")

# Create map
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()], zoom_start=12)

# Function to generate popup content based on the class and dataset
def generate_popup(row):
    if selected_file == "Urban Density":
        return f"Urban Density: {row['label']}"
    elif selected_file == "Land Use":
        return f"Land Use: {row['land_use']}"
    elif selected_file == "Roads":
        return f"Road Type: {row['highway']}"
    elif selected_file == "LCZ":
        return f"LCZ Zone: {row['LCZ_Filter']}"
    elif selected_file == "NDVI":
        return f"NDVI Class: {row['label']}"
    else:
        return "No additional information available"

# Add GeoJSON layer with popups
def add_geojson_layer(gdf, map_obj):
    for _, row in gdf.iterrows():
        geo_json = folium.GeoJson(row['geometry'])
        popup = folium.Popup(generate_popup(row), max_width=300)
        geo_json.add_child(popup)
        geo_json.add_to(map_obj)

# Add layers
if show_all_layers:
    for file_name, file_path in data_files.items():
        layer_gdf = gpd.read_file(file_path)
        add_geojson_layer(layer_gdf, m)
else:
    add_geojson_layer(filtered_gdf, m)

# Add Layer Control
folium.LayerControl().add_to(m)

# Display the map
st_folium(m, width=700, height=500)


















































































