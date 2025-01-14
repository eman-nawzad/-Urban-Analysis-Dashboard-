import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd

# Dictionary to map the names of the files to a label in the sidebar
data_files = {
    "Urban Density": "data/UrbanDensity.geojson",
    "LCZ": "data/LCZ_Zones.geojson",
    "Land Use": "data/Land_Use.geojson",
    "NDVI": "data/NDVIT.geojson",
    "Roads": "data/Roads.geojson"
}

# Sidebar for selecting which dataset to view
st.sidebar.title("Dataset Selector")

# Option to select all layers
show_all_layers = st.sidebar.checkbox("Show All Layers", value=False)

# Dataset selection box
selected_file = st.sidebar.selectbox("Choose a dataset", list(data_files.keys()))

# Load the selected dataset
gdf = gpd.read_file(data_files[selected_file])

# Check if the 'time' column exists
if 'time' in gdf.columns:
    # Ensure the 'time' column is in datetime format
    gdf['time'] = pd.to_datetime(gdf['time'], errors='coerce')

    # Get the min and max date in the data
    min_date_in_data = gdf['time'].min().date()
    max_date_in_data = gdf['time'].max().date()

    # Sidebar date picker
    start_date = st.sidebar.date_input("Start Date", min_value=min_date_in_data, max_value=max_date_in_data)
    end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=max_date_in_data)

    # Filter the dataset based on the selected date range
    filtered_gdf = gdf[(gdf['time'] >= pd.to_datetime(start_date)) & (gdf['time'] <= pd.to_datetime(end_date))]

else:
    st.sidebar.warning("'time' column not found in the selected dataset. No date filtering will be applied.")
    filtered_gdf = gdf  # No date filtering if 'time' column is missing

# Filter based on the selected dataset
if selected_file == "Urban Density":
    # Example: Filter by urban density classes
    density_classes = {
        "Very Low Density (<10%)": 1,
        "Low Density (10–30%)": 2,
        "Medium Density (30–70%)": 3,
        "High Density (>70%)": 4
    }
    selected_density = st.sidebar.selectbox(
        "Filter by Urban Density Class",
        list(density_classes.keys()) + ["All"]
    )
    
    if selected_density == "All":
        filtered_gdf = filtered_gdf
    else:
        selected_density_value = density_classes[selected_density]
        filtered_gdf = filtered_gdf[filtered_gdf['label'] == selected_density_value]

elif selected_file == "LCZ":
    # Map LCZ classes
    lcz_classes = {
        "Compact High-Rise": 1,
        "Open Low-Rise": 6,
        "Industrial Zones": 8
    }
    selected_lcz_class = st.sidebar.selectbox(
        "Filter by LCZ Class",
        list(lcz_classes.keys()) + ["All"]
    )
    
    if selected_lcz_class == "All":
        filtered_gdf = filtered_gdf
    else:
        selected_lcz_value = lcz_classes[selected_lcz_class]
        filtered_gdf = filtered_gdf[filtered_gdf['LCZ_Filter'] == selected_lcz_value]

elif selected_file == "Land Use":
    # Filter Land Use for 2021
    land_use_classes = {
        3: "Croplands",
        4: "Urban",
        6: "Barren"
    }
    st.sidebar.markdown("#### Land Use Data (2021)")
    selected_land_use = st.sidebar.selectbox(
        "Filter by Land Use Class",
        list(land_use_classes.values()) + ["All"]
    )
    
    if selected_land_use == "All":
        filtered_gdf = filtered_gdf[filtered_gdf['land_use'].isin(land_use_classes.keys())]
    else:
        selected_land_use_value = [key for key, value in land_use_classes.items() if value == selected_land_use][0]
        filtered_gdf = filtered_gdf[filtered_gdf['land_use'] == selected_land_use_value]

elif selected_file == "NDVI":
    # Filter NDVI data for 2021
    label_mapping = {
        1: "Dense Forest",
        2: "Sparse Grass"
    }
    st.sidebar.markdown("#### NDVI Data (2021)")
    filtered_gdf = filtered_gdf[filtered_gdf['label'] != 3]  # Remove value 3
    filtered_gdf['label'] = filtered_gdf['label'].map(label_mapping).fillna(filtered_gdf['label'])
    unique_labels = filtered_gdf['label'].unique()
    selected_label = st.sidebar.selectbox(
        "Filter by NDVI Label",
        list(unique_labels) + ["All"]
    )
    
    if selected_label == "All":
        filtered_gdf = filtered_gdf
    else:
        filtered_gdf = filtered_gdf[filtered_gdf['label'] == selected_label]

elif selected_file == "Roads":
    # Filter by road type (highway)
    highway_types = filtered_gdf['highway'].unique()
    selected_highway = st.sidebar.selectbox(
        "Filter by Road Type",
        list(highway_types) + ["All"]
    )
    
    if selected_highway == "All":
        filtered_gdf = filtered_gdf
    else:
        filtered_gdf = filtered_gdf[filtered_gdf['highway'] == selected_highway]

# Sidebar warning message for no data
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected class in the '{selected_file}' dataset. Please try a different selection.")
else:
    st.sidebar.success(f"Displaying data from the '{selected_file}' dataset.")

# Create the map
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()], zoom_start=12)

# Add the filtered GeoJSON data to the map
folium.GeoJson(filtered_gdf, name=selected_file).add_to(m)

# Add a layer control
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)

# Display the filtered dataset in a table below the map
st.write(f"### {selected_file} Dataset")
st.dataframe(filtered_gdf)








































































