import folium
import geopandas as gpd
import streamlit as st
from folium import plugins

# Load the GeoJSON files from the data folder
LCZ = gpd.read_file('data/LCZ.GeoJson.geojson')
land_use = gpd.read_file('data/Land_Use.geojson')
ndvi_ds = gpd.read_file('data/NDVI-DS.geojson')
roads = gpd.read_file('data/Roads.geojson')
urban_density = gpd.read_file('data/UrbanDensity.geojson')

# Define the center of the map (you can update it based on your data's extent)
latitude = 36.324
longitude = 43.968

# Initialize map
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Add LCZ Layer (Local Climate Zones)
LCZ_layer = folium.FeatureGroup(name='LCZ (Local Climate Zones)').add_to(m)
folium.GeoJson(
    LCZ,
    style_function=lambda x: {
        'fillColor': 'lightblue',  # You can customize this color based on the LCZ classification
        'color': 'blue',
        'weight': 1,
        'fillOpacity': 0.6
    }
).add_to(LCZ_layer)

# Add Land Use Layer
land_use_layer = folium.FeatureGroup(name='Land Use').add_to(m)
folium.GeoJson(
    land_use,
    style_function=lambda x: {
        'fillColor': 'green' if x['properties']['Urban Zones (Residential/Commercial)'] == 'Residential' else 'red',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }
).add_to(land_use_layer)

# Add NDVI-DS Layer (Normalized Difference Vegetation Index)
ndvi_ds_layer = folium.FeatureGroup(name='NDVI-DS').add_to(m)
folium.GeoJson(
    ndvi_ds,
    style_function=lambda x: {
        'fillColor': 'yellow' if x['properties']['NDVI'] > 0.3 else 'brown',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }
).add_to(ndvi_ds_layer)

# Add Roads Layer
roads_layer = folium.FeatureGroup(name='Roads').add_to(m)
folium.GeoJson(
    roads,
    style_function=lambda x: {
        'color': 'orange',  # Roads are styled with orange color
        'weight': 2,
        'opacity': 1
    }
).add_to(roads_layer)

# Add Urban Density Layer
urban_density_layer = folium.FeatureGroup(name='Urban Density').add_to(m)
folium.GeoJson(
    urban_density,
    style_function=lambda x: {
        'fillColor': 'blue' if x['properties']['Density'] > 50 else 'yellow',
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }
).add_to(urban_density_layer)

# Add Layer Control (allows the user to toggle visibility of layers)
folium.LayerControl().add_to(m)

# Save map to HTML file
m.save('urban_analysis_map.html')

# Display map in Streamlit
st.title('Urban Analysis Dashboard')
st.markdown("This dashboard displays various urban analysis data layers.")

# Show the map in the Streamlit app
from streamlit_folium import st_folium
st_folium(m, width=800, height=600)

# Provide legend or additional instructions as needed
st.markdown("""
### Legend
- **LCZ (Local Climate Zones):** Blue areas represent Local Climate Zones.
- **Land Use:** Green for Residential, Red for Commercial.
- **NDVI-DS (Normalized Difference Vegetation Index):** Yellow represents healthy vegetation, while brown indicates lower vegetation index.
- **Roads:** Orange color for the road network.
- **Urban Density:** Blue represents high-density areas, yellow indicates lower density.

You can toggle layers on and off using the layer control in the top-right corner of the map.
""")






