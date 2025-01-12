import folium
import geopandas as gpd
import streamlit as st
import os

# Load GeoJSON files from the data folder
LCZ = gpd.read_file('data/LCZ.GeoJson.geojson')
Land_Use = gpd.read_file('data/Land_Use.geojson')
NDVI_DS = gpd.read_file('data/NDVI-DS.geojson')
Roads = gpd.read_file('data/Roads.geojson')
UrbanDensity = gpd.read_file('data/UrbanDensity.geojson')

# Create a base map centered around the first GeoJSON layer's centroid
m = folium.Map(location=[LCZ.geometry.centroid.y.mean(), LCZ.geometry.centroid.x.mean()], zoom_start=12)

# Create FeatureGroups for each GeoJSON layer
lcz_group = folium.FeatureGroup(name="Local Climate Zones")
land_use_group = folium.FeatureGroup(name="Vegetation Distribution")
roads_group = folium.FeatureGroup(name="Roads")
urban_density_group = folium.FeatureGroup(name="Urban Density")

# Define style functions for customized symbols and colors for each layer

# LCZ layer - Customize with different colors for high-rise, low-rise, etc.
def lcz_style(feature):
    lcz_type = feature['properties'].get('LCZ_Type', 'Other')  # Adjust field as per your GeoJSON
    color = 'green' if lcz_type == 'high-rise' else 'blue' if lcz_type == 'low-rise' else 'gray'
    return {
        'fillColor': color,
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }

# Vegetation layer - Different colors for dense forest, grassland, etc.
def vegetation_style(feature):
    land_use_type = feature['properties'].get('Land_Use_Type', 'Other')  # Adjust field as per your GeoJSON
    color = 'darkgreen' if land_use_type == 'dense forest' else 'lightgreen' if land_use_type == 'grassland' else 'lightyellow'
    return {
        'fillColor': color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6
    }

# Roads layer - Different colors for main roads and secondary roads
def roads_style(feature):
    road_type = feature['properties'].get('Road_Type', 'Other')  # Adjust field as per your GeoJSON
    color = 'red' if road_type == 'main road' else 'orange' if road_type == 'secondary road' else 'gray'
    return {
        'color': color,
        'weight': 3
    }

# Urban Density layer - Customize based on population density
def urban_density_style(feature):
    density = feature['properties'].get('Density', 0)  # Adjust field as per your GeoJSON
    color = 'darkblue' if density > 1000 else 'blue' if density > 500 else 'lightblue'
    return {
        'fillColor': color,
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }

# Add GeoJSON layers to the respective FeatureGroups with customized styles
folium.GeoJson(LCZ, style_function=lcz_style).add_to(lcz_group)
folium.GeoJson(Land_Use, style_function=vegetation_style).add_to(land_use_group)
folium.GeoJson(Roads, style_function=roads_style).add_to(roads_group)
folium.GeoJson(UrbanDensity, style_function=urban_density_style).add_to(urban_density_group)

# Add FeatureGroups to the map
lcz_group.add_to(m)
land_use_group.add_to(m)
roads_group.add_to(m)
urban_density_group.add_to(m)

# Add LayerControl to allow toggling between layers
folium.LayerControl().add_to(m)

# Add a title and description to the Streamlit app
st.title("Urban Analysis Dashboard")
st.markdown("""
This dashboard provides insights into various urban parameters such as Local Climate Zones (LCZ), 
Vegetation Distribution, Roads, and Urban Density. Explore these datasets through the interactive map below.
""")

# Save the map to an HTML file
map_file = "temp_map_with_layers.html"
m.save(map_file)

# Use Streamlit's HTML component to render the map
st.components.v1.html(open(map_file, 'r').read(), height=500)

# Clean up the temporary file
os.remove(map_file)



