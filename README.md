# Urban Analysis Dashboard

This is an interactive web dashboard for urban analysis, built using **Streamlit** and **Folium**. The dashboard allows users to visualize various urban-related data layers, including land use, local climate zones, vegetation distribution, roads, and urban density. Each layer can be toggled on/off, and custom colors and symbols are used for better understanding.

## Features

- **Land Use**: Visualizes different land use types, such as residential and commercial areas.
- **Local Climate Zones (LCZ)**: Displays different climate zones, e.g., high-rise and low-rise zones.
- **Vegetation Distribution**: Shows vegetation types like dense forest and grassland.
- **Road Network**: Displays primary and secondary roads with color differentiation.
- **Urban Density**: Visualizes urban density with color variations for different population density zones.

## Requirements

The project requires the following libraries:

- **folium**: For creating interactive maps.
- **streamlit**: For creating the web dashboard.
- **geopandas**: For reading and processing GeoJSON data files.

You can install all required dependencies using the following command:

```bash
pip install -r requirements.txt
git clone https://github.com/eman-nawzad/urban-analysis-dashboard.git
cd urban-analysis-dashboard
pip install -r requirements.txt
streamlit run app.py

Data
This project uses GeoJSON data for various urban-related attributes. The following data files are included:

LCZ.GeoJson.geojson: Local Climate Zones data.
Land_Use.geojson: Land Use data.
NDVI-DS.geojson: Vegetation Distribution data.
Roads.geojson: Road Network data.
UrbanDensity.geojson: Urban Density data.
License
This project is licensed under the MIT License - see the LICENSE file for details.

markdown
Copy code

### Summary of Updates:

1. **`requirements.txt`** includes `folium`, `streamlit`, and `geopandas` for the web and mapping features.
2. **`README.md`** includes project description, features, installation instructions, data description, and usage steps.

You can adjust the `README.md` to fit your project's specifics if needed! Let me know if you need any further assistance.

