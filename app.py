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

# Filter by time if NDVI dataset is selected
if selected_file == "NDVI":
    # Check if 'time' column exists
    if 'time' not in gdf.columns:
        st.error("The dataset does not contain a 'time' column.")
    else:
        # Check if the 'time' column is numeric (timestamp in milliseconds)
        if pd.api.types.is_numeric_dtype(gdf['time']):
            # Convert timestamp (milliseconds since Unix epoch) to datetime
            gdf['time'] = pd.to_datetime(gdf['time'], unit='ms')
        
        # Handle case where 'time' conversion fails
        if gdf['time'].isnull().all():
            st.error("The 'time' column could not be parsed as datetime.")
        else:
            # Add date picker for time range selection
            start_date = st.sidebar.date_input("Start Date", min_value=gdf['time'].min().date(), max_value=gdf['time'].max().date())
            end_date = st.sidebar.date_input("End Date", min_value=start_date, max_value=gdf['time'].max().date())

            # Filter the dataset based on the selected date range
            filtered_gdf = gdf[(gdf['time'] >= pd.to_datetime(start_date)) & (gdf['time'] <= pd.to_datetime(end_date))]

            # Convert the 'time' column to string (ISO 8601 format) to make it JSON serializable
            filtered_gdf['time'] = filtered_gdf['time'].dt.strftime('%Y-%m-%dT%H:%M:%S')

elif selected_file == "Urban Density":
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
        filtered_gdf = gdf
    else:
        selected_density_value = density_classes[selected_density]
        filtered_gdf = gdf[gdf['label'] == selected_density_value]

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
        filtered_gdf = gdf
    else:
        selected_lcz_value = lcz_classes[selected_lcz_class]
        filtered_gdf = gdf[gdf['LCZ_Filter'] == selected_lcz_value]

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
        filtered_gdf = gdf[gdf['land_use'].isin(land_use_classes.keys())]
    else:
        selected_land_use_value = [key for key, value in land_use_classes.items() if value == selected_land_use][0]
        filtered_gdf = gdf[gdf['land_use'] == selected_land_use_value]

elif selected_file == "Roads":
    # Filter by road type (highway)
    highway_types = gdf['highway'].unique()
    selected_highway = st.sidebar.selectbox(
        "Filter by Road Type",
        list(highway_types) + ["All"]
    )
    
    if selected_highway == "All":
        filtered_gdf = gdf
    else:
        filtered_gdf = gdf[gdf['highway'] == selected_highway]

# Sidebar warning message for no data
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected class in the '{selected_file}' dataset. Please try a different selection.")
else:
    st.sidebar.success(f"Displaying data from the '{selected_file}' dataset.")

# Create the map
m = folium.Map(location=[gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()], zoom_start=12)

# Add the filtered GeoJSON data to the map
folium.GeoJson(filtered_gdf.to_json(), name=selected_file).add_to(m)

# Add a layer control
folium.LayerControl().add_to(m)

# Display the map in Streamlit
st_folium(m, width=700, height=500)

# Display the filtered dataset in a table below the map
st.write(f"### {selected_file} Dataset")
st.dataframe(filtered_gdf)







































































