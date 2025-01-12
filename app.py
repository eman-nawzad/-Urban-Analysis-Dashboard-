import folium
import geopandas as gpd

# Read the GeoJSON files
land_use = gpd.read_file('data/Land_Use.geojson')
urban_density = gpd.read_file('data/UrbanDensity.geojson')

# Inspect the columns to check the correct property names
print(land_use.columns)
print(urban_density.columns)

# Initialize map (use a specific location for the initial map view)
latitude = 36.324
longitude = 43.968
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

# Add Layer Control to toggle layers
folium.LayerControl().add_to(m)

# Save map as HTML
m.save('urban_analysis_map.html')





