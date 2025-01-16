Urban Analysis Dashboard


Overview
The Urban Analysis Dashboard is a comprehensive web application designed to provide insights into urban environments through spatial analysis. It integrates data on local climate zones (LCZ), land use, vegetation indices, road networks, and urban density to support urban planning and decision-making.



Repository Structure

data/

├── LCZ.geojson          # Local Climate Zones data

├── Land_Use.geojson     # Land use data

├── NDVIm.geojson        # Normalized Difference Vegetation Index (NDVI) data

├── Roads.geojson        # Road network data

├── UrbanDensity.geojson # Urban density data

README.md                # Project documentation

app.py                   # Main application script

requirements.txt         # Python dependencies








Features

1.Local Climate Zones (LCZ) Analysis
Gain insights into urban thermal environments and microclimates.


2.Land Use Mapping
Analyze land use patterns and their impact on urban sustainability.


3.Vegetation Index Insights
Utilize NDVI data to assess vegetation health and distribution.


4.Road Network Analysis
Examine road density and distribution for urban connectivity.


5.Urban Density Visualization
Explore urbanization trends and population density.








Installation
Clone the repository
git clone https://github.com/eman-nawzad/urban-analysis-Dashboard.git
cd urban-analysis-Dashboard


pip install -r requirements.txt
streamlit run app.py


Access the dashboard
Open the provided URL in your browser to start exploring urban data.



Data Sources
LCZ.geojson: Local Climate Zones from [Source/Provider].
Land_Use.geojson: Land use data from [Source/Provider].
NDVIm.geojson: Vegetation data based on satellite imagery.
Roads.geojson: Road network data sourced from [Source/Provider].
UrbanDensity.geojson: Urban density metrics from [Source/Provider].


License
This project is licensed under the MIT License.







