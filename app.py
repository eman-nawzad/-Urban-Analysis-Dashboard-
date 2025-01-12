import folium
import geopandas as gpd
import streamlit as st

# Define latitude and longitude for the map center (e.g., Erbil or any location of your choice)
latitude = 36.1910  # Example: Erbil latitude
longitude = 43.9983  # Example: Erbil longitude

# Load GeoJSON files
land_use = gpd.read_file('data/Land_Use.geojson')
lcz = gpd.read_file('data/LCZ.GeoJson.geojson')
vegetation = gpd.read_file('data/NDVI-DS.geojson')
roads = gpd.read_file('data/Roads.geojson')
urban_density = gpd.read_file('data/UrbanDensity.geojson')

# Initialize map
m = folium.Map(location=[latitude, longitude], zoom_start=12)

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

# Add Local Climate Zones Layer
lcz_layer = folium.FeatureGroup(name='Local Climate Zones').add_to(m)
folium.GeoJson(
    lcz,
    style_function=lambda x: {
        'fillColor': 'blue' if x['properties']['zone_type'] == 'high-rise' else 'orange',  # Adjust 'zone_type' as needed
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }
).add_to(lcz_layer)

# Add Vegetation Distribution Layer
vegetation_layer = folium.FeatureGroup(name='Vegetation Distribution').add_to(m)
folium.GeoJson(
    vegetation,
    style_function=lambda x: {
        'fillColor': 'green' if x['properties']['vegetation_type'] == 'dense forest' else 'lightgreen',  # Adjust 'vegetation_type' as needed
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }
).add_to(vegetation_layer)

# Add Roads Layer
roads_layer = folium.FeatureGroup(name='Roads').add_to(m)
folium.GeoJson(
    roads,
    style_function=lambda x: {
        'color': 'red' if x['properties']['highway'] == 'primary' else 'blue',  # Adjust 'highway' as needed
        'weight': 2
    }
).add_to(roads_layer)

# Add Urban Density Layer
urban_density_layer = folium.FeatureGroup(name='Urban Density').add_to(m)
folium.GeoJson(
    urban_density,
    style_function=lambda x: {
        'fillColor': 'yellow' if x['properties']['density'] == 'high' else 'lightyellow',  # Adjust 'density' as needed
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }
).add_to(urban_density_layer)

# Add Layer Control
folium.LayerControl().add_to(m)

# Save map to HTML file
m.save('urban_analysis_map.html')

# Optionally, display the map in Streamlit
st.title("Urban Analysis Dashboard")
st.markdown("### Interactive map with different urban analysis layers.")
st.markdown("Use the layer control to toggle between Land Use, Local Climate Zones, Vegetation Distribution, Roads, and Urban Density.")
st.components.v1.html(m._repr_html_(), width=800, height=600)



