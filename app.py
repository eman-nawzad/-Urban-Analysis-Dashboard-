import folium
import geopandas as gpd
import streamlit as st
import os
from folium import plugins

# Load GeoJSON files from the data folder
LCZ = gpd.read_file('data/LCZ.GeoJson.geojson')
Land_Use = gpd.read_file('data/Land_Use.geojson')
NDVI_DS = gpd.read_file('data/NDVI-DS.geojson')
Roads = gpd.read_file('data/Roads.geojson')
UrbanDensity = gpd.read_file('data/UrbanDensity.geojson')

# Create a base map centered around the first GeoJSON layer's centroid
m = folium.Map(location=[LCZ.geometry.centroid.y.mean(), LCZ.geometry.centroid.x.mean()], zoom_start=12)

# Sidebar for filtering
st.sidebar.title("Filter Controls")

# Example Filters: Change based on your actual data
selected_lcz_type = st.sidebar.selectbox("Select LCZ Type", ["All", "high-rise", "low-rise", "other"])
selected_land_use_type = st.sidebar.selectbox("Select Land Use", ["All", "dense forest", "grassland", "urban"])
selected_road_type = st.sidebar.selectbox("Select Road Type", ["All", "main road", "secondary road"])
selected_density_range = st.sidebar.slider("Select Population Density", 0, 10000, (0, 10000))

# Filter data based on user input
filtered_lcz = LCZ[LCZ['LCZ_Type'].str.contains(selected_lcz_type, case=False, na=False)] if selected_lcz_type != "All" else LCZ
filtered_land_use = Land_Use[Land_Use['Land_Use_Type'].str.contains(selected_land_use_type, case=False, na=False)] if selected_land_use_type != "All" else Land_Use
filtered_roads = Roads[Roads['Road_Type'].str.contains(selected_road_type, case=False, na=False)] if selected_road_type != "All" else Roads
filtered_urban_density = UrbanDensity[(UrbanDensity['Density'] >= selected_density_range[0]) & (UrbanDensity['Density'] <= selected_density_range[1])]

# Create FeatureGroups for each GeoJSON layer
lcz_group = folium.FeatureGroup(name="Local Climate Zones")
land_use_group = folium.FeatureGroup(name="Land Use")
ndvi_group = folium.FeatureGroup(name="NDVI")
roads_group = folium.FeatureGroup(name="Roads")
urban_density_group = folium.FeatureGroup(name="Urban Density")

# Define style functions for customized symbols and colors for each layer
def lcz_style(feature):
    lcz_type = feature['properties'].get('LCZ_Type', 'Other')
    color = 'green' if lcz_type == 'high-rise' else 'blue' if lcz_type == 'low-rise' else 'gray'
    return {
        'fillColor': color,
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }

def land_use_style(feature):
    land_use_type = feature['properties'].get('Land_Use_Type', 'Other')
    color = 'darkgreen' if land_use_type == 'dense forest' else 'lightgreen' if land_use_type == 'grassland' else 'lightyellow'
    return {
        'fillColor': color,
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.6
    }

def roads_style(feature):
    road_type = feature['properties'].get('Road_Type', 'Other')
    color = 'red' if road_type == 'main road' else 'orange' if road_type == 'secondary road' else 'gray'
    return {
        'color': color,
        'weight': 3
    }

def urban_density_style(feature):
    density = feature['properties'].get('Density', 0)
    color = 'darkblue' if density > 1000 else 'blue' if density > 500 else 'lightblue'
    return {
        'fillColor': color,
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5
    }

# Function to add GeoJSON to FeatureGroups with hover info and filtering
def add_geojson_to_map(geojson_data, group, style_func, hover_info_func=None):
    folium.GeoJson(geojson_data, style_function=style_func, tooltip=hover_info_func).add_to(group)

# Add GeoJSON layers to the map based on filtered data
add_geojson_to_map(filtered_lcz, lcz_group, lcz_style, lambda feature: f"LCZ Type: {feature['properties'].get('LCZ_Type', 'N/A')}")
add_geojson_to_map(filtered_land_use, land_use_group, land_use_style, lambda feature: f"Land Use: {feature['properties'].get('Land_Use_Type', 'N/A')}")
add_geojson_to_map(filtered_roads, roads_group, roads_style, lambda feature: f"Road Type: {feature['properties'].get('Road_Type', 'N/A')}")
add_geojson_to_map(filtered_urban_density, urban_density_group, urban_density_style, lambda feature: f"Density: {feature['properties'].get('Density', 'N/A')}")

# Add FeatureGroups to the map
lcz_group.add_to(m)
land_use_group.add_to(m)
ndvi_group.add_to(m)
roads_group.add_to(m)
urban_density_group.add_to(m)

# Add Layer Control to toggle between layers
folium.LayerControl().add_to(m)

# Title and description for the app
st.title("Urban Analysis Dashboard")
st.markdown("""
Explore various urban analysis metrics such as Local Climate Zones (LCZ), Vegetation Distribution, 
Road Types, and Urban Density with filtering controls for dynamic updates.
""")

# Save the map to an HTML file and render it with Streamlit
map_file = "interactive_map_with_filtering.html"
m.save(map_file)

# Display map in Streamlit app
st.components.v1.html(open(map_file, 'r').read(), height=500)

# Clean up the temporary file
os.remove(map_file)




