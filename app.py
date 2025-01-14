import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Dictionary to map the names of the files to a label in the sidebar
data_files = {
    "Urban Density": "data/UrbanDensity.geojson",
    "LCZ": "data/LCZ_Zones.geojson",
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
        list(density_classes.keys()) + ["All"]
    )
    
    if selected_density == "All":
        filtered_gdf = gdf
    else:
        selected_density_value = density_classes[selected_density]
        filtered_gdf = gdf[gdf['label'] == selected_density_value]

elif selected_file == "LCZ_Zones":
    # Map the LCZ class names to their corresponding numerical values
    lcz_classes = {
        "Compact High-Rise": 1,
        "Open Low-Rise": 6,
        "Industrial Zones": 8
    }
    
    # Sidebar selectbox now displays the class names plus "All" option
    selected_lcz_class = st.sidebar.selectbox(
        "Filter by LCZ Class",
        list(lcz_classes.keys()) + ["All"]
    )
    
    if selected_lcz_class == "All":
        filtered_gdf = gdf
    else:
        # Get the numerical value for the selected LCZ class
        selected_lcz_value = lcz_classes[selected_lcz_class]
        
        # Filter by the corresponding numerical value in 'LCZ_Filter' column
        filtered_gdf = gdf[gdf['LCZ_Filter'] == selected_lcz_value]

elif selected_file == "Land Use":
    # Replace land use class values with their corresponding names
    land_use_classes = {
        3: "Croplands",
        4: "Urban",
        6: "Barren"
    }
    
    selected_land_use = st.sidebar.selectbox(
        "Filter by Land Use Class",
        list(land_use_classes.values()) + ["All"]
    )
    
    if selected_land_use == "All":
        filtered_gdf = gdf[gdf['land_use'].isin(land_use_classes.keys())]
    else:
        selected_land_use_value = [key for key, value in land_use_classes.items() if value == selected_land_use][0]
        filtered_gdf = gdf[gdf['land_use'] == selected_land_use_value]
        
elif selected_file == "NDVI":
    # Replace numeric values with names in the 'label' column for NDVI
    if 'label' in gdf.columns:
        # Replace values with names: 1 -> "Dense Forest", 2 -> "Sparse Grass"
        label_mapping = {
            1: "Dense Forest",
            2: "Sparse Grass"
        }
        gdf['label'] = gdf['label'].map(label_mapping).fillna(gdf['label'])

        # Filter by the 'label' column for NDVI
        unique_labels = gdf['label'].unique()
        selected_label = st.sidebar.selectbox(
            "Filter by NDVI Label",
            list(unique_labels) + ["All"]
        )
        
        if selected_label == "All":
            filtered_gdf = gdf
        else:
            filtered_gdf = gdf[gdf['label'] == selected_label]
    else:
        filtered_gdf = gdf  # If 'label' column doesn't exist, display the whole dataset

elif selected_file == "Roads":
    # Filter by highway types (road types)
    if 'highway' in gdf.columns:
        highway_types = gdf['highway'].unique()
        selected_highway = st.sidebar.selectbox(
            "Filter by Road Type (Highway)",
            list(highway_types) + ["All"]
        )
        
        if selected_highway == "All":
            filtered_gdf = gdf
        else:
            filtered_gdf = gdf[gdf['highway'] == selected_highway]
    else:
        filtered_gdf = gdf

else:
    filtered_gdf = gdf

# Sidebar warning message for no data
if filtered_gdf.empty:
    st.sidebar.warning(f"No data available for the selected filter in the '{selected_file}' dataset. Please try a different combination.")
else:
    st.sidebar.success(f"Displaying data from the '{selected_file}' dataset.")

# Create a Folium map centered around the filtered data
m = folium.Map(location=[filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()],
               zoom_start=12)

# Add the selected layer
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
    add_layer(gpd.read_file(data_files["Land Use"]), "Land Use", color="orange")
    add_layer(gpd.read_file(data_files["NDVI"]), "NDVI", color="green")
    add_layer(gpd.read_file(data_files["Roads"]), "Roads", color="red")
else:
    # Add only the selected dataset to the map
    if selected_file == "Urban Density":
        add_layer(filtered_gdf, "Urban Density", color="black")
    elif selected_file == "LCZ":
        add_layer(filtered_gdf, "LCZ", color="blue")
    elif selected_file == "Land Use":
        add_layer(filtered_gdf, "Land Use", color="orange")
    elif selected_file == "NDVI":
        add_layer(filtered_gdf, "NDVI", color="green")
    elif selected_file == "Roads":
        add_layer(filtered_gdf, "Roads", color="red")

# Add a layer control to toggle layers on/off
folium.LayerControl().add_to(m)

# Show the map in Streamlit
st_folium(m, width=700, height=500)

# Display the filtered dataset as a table below the map
st.write(f"### {selected_file} Dataset")
st.dataframe(filtered_gdf)  # Show the filtered data as a table below the map































































