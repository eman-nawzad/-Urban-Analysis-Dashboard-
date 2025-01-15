import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Define dataset paths
data_files = {
    "Urban Density": "data/UrbanDensity.geojson",
    "LCZ": "data/LCZ.geojson",
    "Land Use": "data/Land_Use.geojson",
    "NDVI": "data/NDVIm.geojson",  # Ensure the correct NDVI GeoJSON path
    "Roads": "data/Roads.geojson"
}

# Define the classes for each dataset
density_classes = {
    1: "Very Low Density (<10%)",
    2: "Low Density (10–30%)",
    3: "Medium Density (30–70%)",
    4: "High Density (>70%)"
}

land_use_classes = {
    3: "Croplands",
    4: "Urban",
    6: "Barren"
}

lcz_classes = {
    1: "Compact High-Rise",
    6: "Open Low-Rise",
    8: "Industrial Zones"
}

# NDVI Classes
ndvi_classes = {
    1: "Dense Forest ",
    2: "Sparse Grass "
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
    density_filter = st.sidebar.selectbox(
        "Filter by Urban Density Class", ["All"] + list(density_classes.values())
    )
    if density_filter != "All":
        class_value = list(density_classes.values()).index(density_filter) + 1  # Mapping to numeric values
        filtered_gdf = gdf[gdf['label'] == class_value]

elif selected_file == "LCZ":
    lcz_filter = st.sidebar.selectbox("Filter by LCZ Class", ["All"] + list(lcz_classes.values()))
    if lcz_filter != "All":
        class_value = [key for key, value in lcz_classes.items() if value == lcz_filter][0]
        filtered_gdf = gdf[gdf['LCZ_Filter'] == class_value]

elif selected_file == "Land Use":
    land_use_filter = st.sidebar.selectbox(
        "Filter by Land Use Class", ["All"] + list(land_use_classes.values())
    )
    if land_use_filter != "All":
        class_value = [k for k, v in land_use_classes.items() if v == land_use_filter][0]
        filtered_gdf = gdf[gdf['land_use'] == class_value]

elif selected_file == "NDVI":
    if 'label' in gdf.columns:
        ndvi_filter = st.sidebar.selectbox("Filter by NDVI Class", ["All"] + list(ndvi_classes.values()))
        if ndvi_filter != "All":
            class_value = list(ndvi_classes.values()).index(ndvi_filter) + 1  # Mapping to numeric values
            filtered_gdf = gdf[gdf['label'] == class_value]

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

# Function to generate popups with class names instead of raw values
def generate_popup(row, dataset_name):
    popup_content = f"<strong>Feature Information</strong><br>"
    if dataset_name == "Urban Density":
        density_class = density_classes.get(row['label'], "Unknown")
        popup_content += f"<b>Urban Density:</b> {density_class}<br>"
    elif dataset_name == "Land Use":
        land_use_class = land_use_classes.get(row['land_use'], "Unknown")
        popup_content += f"<b>Land Use:</b> {land_use_class}<br>"
    elif dataset_name == "Roads":
        road_type = row.get('highway', "Unknown")
        popup_content += f"<b>Road Type:</b> {road_type}<br>"
    elif dataset_name == "LCZ":
        lcz_class = lcz_classes.get(row['LCZ_Filter'], "Unknown")
        popup_content += f"<b>LCZ Class:</b> {lcz_class}<br>"
    elif dataset_name == "NDVI":
        ndvi_class = ndvi_classes.get(row['label'], "Unknown")
        popup_content += f"<b>NDVI Class:</b> {ndvi_class}<br>"
    return popup_content

# Function to get styling based on dataset
def get_style_function(dataset_name):
    if dataset_name == "Roads":
        return lambda x: {"color": "red", "weight": 3}  # Roads in red
    else:
        return lambda x: {"color": "blue", "weight": 1}  # Default styling

# Add GeoJSON layer with popups
def add_geojson_layer(gdf, map_obj, dataset_name):
    geo_json = folium.GeoJson(
        gdf.geometry,
        style_function=get_style_function(dataset_name),
        name=dataset_name  # Set the name for LayerControl
    )
    for _, row in gdf.iterrows():
        popup = folium.Popup(generate_popup(row, dataset_name), max_width=300)
        geo_json.add_child(popup)
    geo_json.add_to(map_obj)

# Add layers
if show_all_layers:
    for file_name, file_path in data_files.items():
        layer_gdf = gpd.read_file(file_path)
        add_geojson_layer(layer_gdf, m, file_name)
else:
    add_geojson_layer(filtered_gdf, m, selected_file)

folium.LayerControl().add_to(m)

# Display the map
st_folium(m, width=700, height=500)






















































































