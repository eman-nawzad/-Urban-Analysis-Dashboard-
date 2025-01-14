import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

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

# Dataset selection box
selected_file = st.sidebar.selectbox(
    "Choose a dataset",
    list(data_files.keys())
)

# Load the selected dataset
gdf = gpd.read_file(data_files[selected_file])

# Filter based on the selected dataset (this can be customized based on attributes)
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
        list(density_classes.keys())
    )
    selected_density_value = density_classes[selected_density]
    filtered_gdf = gdf[gdf['label'] == selected_density_value]

elif selected_file == "LCZ":
    # Example: Filter by LCZ (if applicable)
    # If there's a column like 'lcz_class', you can filter it
    if 'lcz_class' in gdf.columns:
        lcz_classes = gdf['lcz_class'].unique()
        selected_lcz = st.sidebar.selectbox(
            "Filter by LCZ Class",
            list(lcz_classes)
        )
        filtered_gdf = gdf[gdf['lcz_class'] == selected_lcz]
    else:
        filtered_gdf = gdf

elif selected_file == "Land Use":
    # Example: Filter by land use class
    if 'land_use' in gdf.columns:
        land_use_classes = gdf['land_use'].unique()
        selected_land_use = st.sidebar.selectbox(
            "Filter by Land Use Class",
            list(land_use_classes)
        )
        filtered_gdf = gdf[gdf['land_use'] == selected_land_use]
    else:
        filtered_gdf = gdf

elif selected_file == "NDVI":
    # Example: Filter by NDVI values (if applicable)
    if 'NDVI' in gdf.columns:
        ndvi_range = st.sidebar.slider(
            "Filter by NDVI Value",
            min_value=gdf['NDVI'].min(),
            max_value=gdf['NDVI'].max(),
            value=(gdf['NDVI'].min(), gdf['NDVI'].max())
        )
        filtered_gdf = gdf[(gdf['NDVI'] >= ndvi_range[0]) & (gdf['NDVI'] <= ndvi_range[1])]
    else:
        filtered_gdf = gdf

else:
    filtered_gdf = gdf

# Show instructions if the data file is empty
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected filter in the '{selected_file}' dataset. Please try a different combination.")
else:
    # Show a success message when data is available
    st.sidebar.success(f"Displaying data from the '{selected_file}' dataset.")

    # Create a Folium map centered around the filtered data
    m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()],
                   zoom_start=12)
    folium.GeoJson(filtered_gdf).add_to(m)
    st_folium(m, width=700, height=500)

















































