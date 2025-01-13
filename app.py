import streamlit as st
import folium
import geopandas as gpd
from folium import plugins
from streamlit_folium import st_folium

# Predefined paths for your GeoJSON files
land_use_path = "path/to/your/land_use.geojson"  # Update this with the correct path
lcz_path = "path/to/your/lcz.geojson"  # Update this with the correct path
ndvi_path = "path/to/your/ndvi.geojson"  # Update this with the correct path
roads_path = "path/to/your/roads.geojson"  # Update this with the correct path
urban_density_path = "path/to/your/urban_density.geojson"  # Update this with the correct path

# Load GeoJSON data from predefined paths
land_use_data = gpd.read_file(land_use_path)
lcz_data = gpd.read_file(lcz_path)
ndvi_data = gpd.read_file(ndvi_path)
road_data = gpd.read_file(roads_path)
urban_density_data = gpd.read_file(urban_density_path)

# Print data structures to check keys (optional)
st.write("Land Use GeoJSON Structure:")
st.write(land_use_data.head())  # Check the structure of the GeoDataFrame

st.write("LCZ GeoJSON Structure:")
st.write(lcz_data.head())

st.write("NDVI GeoJSON Structure:")
st.write(ndvi_data.head())

st.write("Roads GeoJSON Structure:")
st.write(road_data.head())

st.write("Urban Density GeoJSON Structure:")
st.write(urban_density_data.head())

# Define custom colors for each layer
color_palettes = {
    "Land Use": {
        'Residential': 'lightblue', 
        'Commercial': 'lightyellow', 
        'Industrial': 'lightgray'
    },
    "Local Climate Zones (LCZ)": {
        'Compact High-Rise': 'red', 
        'Open Low-Rise': 'green', 
        'Industrial Zones': 'purple'
    },
    "Vegetation (NDVI)": {
        'Dense Forest': 'darkgreen', 
        'Sparse Grass': 'lightgreen'
    },
    "Roads": {
        'primary': 'blue', 
        'motorway': 'green', 
        'trunk': 'orange', 
        'secondary': 'red',
        'main': 'purple'
    },
    "Urban Density": {
        'High': 'darkred', 
        'Medium': 'orange', 
        'Low': 'lightgreen', 
        'Very Low': 'lightblue'
    }
}

# Function to style layers based on custom colors
def style_function(feature, layer_type):
    try:
        # Print the properties of the feature to inspect the structure
        st.write(f"Feature properties: {feature['properties']}")
        
        # Try to get the value from feature properties
        property_value = feature['properties'].get(layer_type, None)
        if property_value:
            # Apply the color based on the property value
            return {
                'fillColor': color_palettes[layer_type].get(property_value, 'gray'),
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
        else:
            # Default color if the property value is missing
            return {
                'fillColor': 'gray',  # Default color
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.7
            }
    except KeyError as e:
        st.error(f"Error: {e}")
        return {
            'fillColor': 'gray',  # Default color for unknown properties
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.7
        }

# Initialize map
m = folium.Map(location=[latitude, longitude], zoom_start=10)

# Add selected layers to the map
selected_layers = ['Land Use', 'Local Climate Zones (LCZ)', 'Vegetation (NDVI)', 'Roads', 'Urban Density']

if "Land Use" in selected_layers:
    folium.GeoJson(
        land_use_data,
        style_function=lambda feature: style_function(feature, "Land Use")
    ).add_to(m)

if "Local Climate Zones (LCZ)" in selected_layers:
    folium.GeoJson(
        lcz_data,
        style_function=lambda feature: style_function(feature, "Local Climate Zones (LCZ)")
    ).add_to(m)

if "Vegetation (NDVI)" in selected_layers:
    folium.GeoJson(
        ndvi_data,
        style_function=lambda feature: style_function(feature, "Vegetation (NDVI)")
    ).add_to(m)

if "Roads" in selected_layers:
    folium.GeoJson(
        road_data,
        style_function=lambda feature: style_function(feature, "Roads")
    ).add_to(m)

if "Urban Density" in selected_layers:
    folium.GeoJson(
        urban_density_data,
        style_function=lambda feature: style_function(feature, "Urban Density")
    ).add_to(m)

# Display map in Streamlit
st_folium(m, width=700, height=500)























