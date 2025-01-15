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

├── tst.txt              # Test or temporary file

README.md               # Project documentation

app.py                  # Main application script

requirements.txt        # Python dependencies










Features

Local Climate Zones (LCZ) Analysis: Understand urban thermal environments and microclimates.

Land Use Mapping: Analyze land use patterns and their impact on urban sustainability.

Vegetation Index Insights: Utilize NDVI data to assess vegetation health and distribution.

Road Network Analysis: Examine road density and distribution for urban connectivity.

Urban Density Visualization: Explore urbanization trends and population density.










Installation

Clone the repository:

git clone https://github.com/eman-nawzad/urban-analysis.git
cd urban-analysis

Set up a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate # On Windows, use venv\Scripts\activate

Install the required dependencies:

pip install -r requirements.txt












Usage

Run the application:

streamlit run app.py

Open the provided URL in your browser to access the dashboard.




Data Sources

LCZ.geojson: Local Climate Zones from [Source/Provider].

Land_Use.geojson: Land use data from [Source/Provider].

NDVIm.geojson: Vegetation data based on satellite imagery.

Roads.geojson: Road network data sourced from [Source/Provider].

UrbanDensity.geojson: Urban density metrics from [Source/Provider].

Contributing

Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch for your feature or bug fix.

Submit a pull request with a detailed description of your changes.










License

This project is licensed under the MIT License.

