import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd
import pandas as pd

# Dictionary to map the names of the files to a label in the sidebar
data_files = {
    "Urban Density": "data/UrbanDensity.geojson",
    "LCZ": "data/LCZ.geojson",
    "Land Use": "data/Land_Use.geojson",
    "NDVI": "data/NDVIt.geojson",
    "Roads": "data/Roads.geojson"
}

# Sidebar for selecting which dataset to view
st.sidebar.title("Select Dataset and Apply Filters")

# Option to select all layers
show_all_layers = st.sidebar.checkbox("Show All Layers", value=False)

# Dataset selection box
selected_file = st.sidebar.selectbox(
    "Choose a dataset",
    list(data_files.keys())
)

# Load the selected dataset
gdf = gpd.read_file(data_files[selected_file])

# Display the data table of the selected layer
st.write(f"### Preview of {selected_file} Dataset")
st.write(gdf.head())  # Show the first few rows of the selected dataset

# Show the column names of the dataset (helpful for filtering)
st.write("### Available Columns for Filtering")
st.write(gdf.columns)

# If the user wants to filter, they can select from the columns
# Create a filter sidebar option based on the available columns
filter_column = st.sidebar.selectbox("Select a column to filter by", gdf.columns)

# Now allow the user to filter based on the selected column (for example, numeric or categorical values)
if gdf[filter_column].dtype == 'object':  # If the column is categorical
    unique_values = gdf[filter_column].unique()
    selected_value = st.sidebar.selectbox(f"Filter by {filter_column}", unique_values)
    filtered_gdf = gdf[gdf[filter_column] == selected_value]
elif gdf[filter_column].dtype in ['int64', 'float64']:  # If the column is numeric
    min_value, max_value = gdf[filter_column].min(), gdf[filter_column].max()
    selected_range = st.sidebar.slider(f"Filter by {filter_column}", min_value, max_value, (min_value, max_value))
    filtered_gdf = gdf[(gdf[filter_column] >= selected_range[0]) & (gdf[filter_column] <= selected_range[1])]
else:
    filtered_gdf = gdf

# Show instructions if the data file is empty after filtering
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected filter in the '{selected_file}' dataset. Please try a different combination.")
else:
    # Show a success message when data is available
    st.sidebar.success(f"Displaying filtered data from the '{selected_file}' dataset.")

# Create a Folium map centered around the filtered data
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()],
               zoom_start=12)

# Add the selected layer to the map with a color (you can change the color as needed)
def add_layer(gdf, layer_name, color=None):
    """Function to add a layer with a specific color if provided."""
    if color:
        folium.GeoJson(gdf, name=layer_name, style_function=lambda x: {'color': color}).add_to(m)
    else:
        folium.GeoJson(gdf, name=layer_name).add_to(m)

# If "Show All Layers" is selected, add all layers with specific colors
if show_all_layers:
    add_layer(gpd.read_file(data_files["Urban Density"]), "Urban Density", color="black")
    add_layer(gpd.read_file(data_files["LCZ"]), "LCZ", color="blue")
    add_layer(gpd.read_file(data_files["Land Use"]), "Land Use", color=" orange")
    add_layer(gpd.read_file(data_files["NDVI"]), "NDVI", color="light green ")
    add_layer(gpd.read_file(data_files["Roads"]), "Roads", color="red")
else:
    # Add only the selected dataset to the map
    if selected_file == "Urban Density":
        add_layer(filtered_gdf, "Urban Density", color="black")
    elif selected_file == "LCZ":
        add_layer(filtered_gdf, "LCZ", color="blue ")
    elif selected_file == "Land Use":
        add_layer(filtered_gdf, "Land Use", color="orange")
    elif selected_file == "NDVI":
        add_layer(filtered_gdf, "NDVI", color="light green")
    elif selected_file == "Roads":
        add_layer(filtered_gdf, "Roads", color="red")

# Add a layer control to toggle layers on/off
folium.LayerControl().add_to(m)

# Show the map in Streamlit
st_folium(m, width=700, height=500)



















































