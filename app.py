import streamlit as st
import folium
from streamlit_folium import st_folium
import geopandas as gpd

# Dictionary to map the names of the files to a label in the sidebar
data_files = {
    "Urban Density": "data/UrbanDensity.geojson",
    "LCZ": "data/LCZ_Zones.geojson",
    "Land Use": "data/Land_Use.geojson",
    "NDVI": "data/NDVIm.geojson",
    "Roads": "data/Roads.geojson"
}

# Sidebar for selecting which dataset to view
st.sidebar.title("Select Dataset and Apply Filters")

# Option to select all layers
show_all_layers = st.sidebar.checkbox("Show All Layers", value=False)

# Dataset selection box
selected_file = st.sidebar.selectbox(
    "Choose a dataset",
    list(data_files.keys())
)

# Load the selected dataset
gdf = gpd.read_file(data_files[selected_file])

# Check if the dataset is empty or has no geometries
if gdf.empty or gdf.geometry.is_empty.all():
    st.error(f"The dataset '{selected_file}' is empty or has no geometries.")
else:
    # Filter based on the selected dataset
    if selected_file == "Urban Density":
        density_classes = {
            "Very Low Density (<10%)": 1,
            "Low Density (10–30%)": 2,
            "Medium Density (30–70%)": 3,
            "High Density (>70%)": 4
        }
        selected_density = st.sidebar.selectbox(
            "Filter by Urban Density Class",
            list(density_classes.keys()) + ["All"]
        )

        if selected_density == "All":
            filtered_gdf = gdf
        else:
            selected_density_value = density_classes[selected_density]
            filtered_gdf = gdf[gdf['label'] == selected_density_value]

    elif selected_file == "LCZ":
        lcz_classes = {
            "Compact High-Rise": 1,
            "Open Low-Rise": 6,
            "Industrial Zones": 8
        }

        selected_lcz_class = st.sidebar.selectbox(
            "Filter by LCZ Class",
            list(lcz_classes.keys()) + ["All"]
        )

        if selected_lcz_class == "All":
            filtered_gdf = gdf
        else:
            selected_lcz_value = lcz_classes[selected_lcz_class]
            filtered_gdf = gdf[gdf['LCZ_Filter'] == selected_lcz_value]

    elif selected_file == "Land Use":
        land_use_classes = {
            3: "Croplands",
            4: "Urban",
            6: "Barren"
        }

        selected_land_use = st.sidebar.selectbox(
            "Filter by Land Use Class",
            list(land_use_classes.values()) + ["All"]
        )

        if selected_land_use == "All":
            filtered_gdf = gdf[gdf['land_use'].isin(land_use_classes.keys())]
        else:
            selected_land_use_value = [key for key, value in land_use_classes.items() if value == selected_land_use][0]
            filtered_gdf = gdf[gdf['land_use'] == selected_land_use_value]

    elif selected_file == "NDVI":
        if 'label' in gdf.columns:
            gdf = gdf[gdf['label'] != 3]
            label_mapping = {
                1: "Dense Forest",
                2: "Sparse Grass"
            }
            gdf['label'] = gdf['label'].map(label_mapping).fillna(gdf['label'])

            unique_labels = gdf['label'].unique()
            selected_label = st.sidebar.selectbox(
                "Filter by NDVI Label",
                list(unique_labels) + ["All"]
            )

            if selected_label == "All":
                filtered_gdf = gdf
            else:
                filtered_gdf = gdf[gdf['label'] == selected_label]
        else:
            filtered_gdf = gdf

    elif selected_file == "Roads":
        if 'highway' in gdf.columns:
            highway_types = gdf['highway'].unique()
            selected_highway = st.sidebar.selectbox(
                "Filter by Road Type (Highway)",
                list(highway_types) + ["All"]
            )

            if selected_highway == "All":
                filtered_gdf = gdf
            else:
                filtered_gdf = gdf[gdf['highway'] == selected_highway]
        else:
            filtered_gdf = gdf

    else:
        filtered_gdf = gdf

    # Create a Folium map centered around the filtered data
    map_center = [filtered_gdf.geometry.centroid.y.mean(), filtered_gdf.geometry.centroid.x.mean()]
    m = folium.Map(location=map_center, zoom_start=12)

    # Define the function to style features
    def style_function(feature):
        return {
            'color': 'blue',
            'weight': 2,
            'opacity': 1
        }

    # Add hover functionality for all datasets
    def add_tooltip(geojson):
        # Add custom tooltips based on columns relevant to each dataset
        if selected_file == "Urban Density":
            geojson.add_child(
                folium.features.GeoJsonTooltip(
                    fields=["label"],
                    aliases=["Urban Density Class"],
                    localize=True
                )
            )
        elif selected_file == "LCZ":
            geojson.add_child(
                folium.features.GeoJsonTooltip(
                    fields=["LCZ_Filter", "zone_type"],
                    aliases=["LCZ Class", "Zone Type"],
                    localize=True
                )
            )
        elif selected_file == "Land Use":
            geojson.add_child(
                folium.features.GeoJsonTooltip(
                    fields=["land_use", "area_type"],
                    aliases=["Land Use Class", "Area Type"],
                    localize=True
                )
            )
        elif selected_file == "NDVI":
            geojson.add_child(
                folium.features.GeoJsonTooltip(
                    fields=["label", "ndvi_value"],
                    aliases=["NDVI Class", "NDVI Value"],
                    localize=True
                )
            )
        elif selected_file == "Roads":
            geojson.add_child(
                folium.features.GeoJsonTooltip(
                    fields=["highway", "road_name"],
                    aliases=["Road Type", "Road Name"],
                    localize=True
                )
            )

    # Add layers based on the "Show All Layers" checkbox
    if show_all_layers:
        # Show all layers
        for file_name, file_path in data_files.items():
            layer_gdf = gpd.read_file(file_path)
            geojson = folium.GeoJson(
                layer_gdf,
                name=file_name,
                style_function=style_function
            )
            add_tooltip(geojson)  # Automatically add tooltip for each dataset
            geojson.add_to(m)
    else:
        # Add only the selected dataset to the map
        geojson = folium.GeoJson(
            filtered_gdf,
            name=selected_file,
            style_function=style_function
        )
        add_tooltip(geojson)  # Automatically add tooltip for the selected dataset
        geojson.add_to(m)

    # Add a layer control to toggle layers on/off
    folium.LayerControl().add_to(m)

    # Show the map in Streamlit
    st_folium(m, width=700, height=500)

    # Display the filtered dataset as a table below the map
    st.write(f"### {selected_file} Dataset")
    st.dataframe(filtered_gdf)













































































