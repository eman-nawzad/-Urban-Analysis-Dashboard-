import folium
from streamlit_folium import st_folium

# Create a simple map centered at a specific location
m = folium.Map(location=[37.7749, -122.4194], zoom_start=12)  # Coordinates for San Francisco

# Display the map
st_folium(m, width=700, height=500)








































