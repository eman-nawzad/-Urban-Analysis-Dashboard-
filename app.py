import folium
import geopandas as gpd
import streamlit as st
from folium import GeoJson

# Load GeoJSON files from the data folder
LCZ = gpd.read_file('data/LCZ.GeoJson.geojson')
land_use = gpd.read_file('data/Land_Use.geojson')
ndvi_ds = gpd.read_file('data/NDVI-DS.geojson')
roads = gpd.read_file('data/Roads.geojson')
urban_density = gpd.read_file('data/UrbanDensity.geojson')

# Create a folium map centered at a specific latitude and longitude
m = folium.Map(location=[36.325735, 43.393432], zoom_start=12)

# Function to safely get the value of the 'Urban Zones (Residential/Commercial)' key
def get_urban_zone(feature):
    return feature['properties'].get('Urban Zones (Residential/Commercial)', 'Unknown')

# Plot LCZ data
GeoJson(
    LCZ,
    style_function=lambda x: {
        'fillColor': 'lightblue',
        'color': 'blue',
        'weight': 0.5,
        'fillOpacity': 0.6,
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['LCZ']),
).add_to(m)

# Plot Land Use data
GeoJson(
    land_use,
    style_function=lambda x: {
        'fillColor': 'green',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5,
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Land Use']),
).add_to(m)

# Plot NDVI-DS data
GeoJson(
    ndvi_ds,
    style_function=lambda x: {
        'fillColor': 'yellow',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5,
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['NDVI-DS']),
).add_to(m)

# Plot Roads data
GeoJson(
    roads,
    style_function=lambda x: {
        'color': 'orange',
        'weight': 2,
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Roads']),
).add_to(m)

# Plot Urban Density data with error handling for missing 'Urban Zones (Residential/Commercial)' key
GeoJson(
    urban_density,
    style_function=lambda x: {
        'fillColor': 'green' if get_urban_zone(x) == 'Residential' else 'red',
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.5,
    },
    tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Urban Density']),
).add_to(m)

# Show the map in Streamlit
st.title('Urban Analysis Dashboard')
st.markdown('This dashboard visualizes various urban features including LCZ, Land Use, NDVI-DS, Roads, and Urban Density.')

# Display the folium map in Streamlit
st.markdown("### Interactive Map")
folium_static(m)






