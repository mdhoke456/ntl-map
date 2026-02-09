# ntl-map
A night time map is generated and visualised as an leafmap.

# Data Requirements
To run the script, place your data in a data/ folder:

data/viirs.tif: VIIRS NTL Nighttime Day/Night Band (DNB) raster.

data/Pune.geojson: Vector file containing ward boundaries for Pune.

Usage
Run the analysis script:

The script will output a file named index.html

🗺️ Visualization Details
The map uses a Dark Matter tile set to emphasize the light data. Wards are styled based on their NTL mean value:

Note: The script includes interactive tooltips showing the Ward Name (NAME_3) and the exact Mean NTL value for precise data inspection.

🛠️ Technical Stack
Raster Processing: rioxarray (Xarray extension for geospatial data).

Vector Analysis: geopandas.

Spatial Stats: rasterstats (Standard for zonal statistics).

Mapping: folium.

📜 Data Sources
Satellite Imagery: VIIRS Day/Night Band (DNB) from NASA/NOAA.

Boundaries: Administrative ward boundaries for Pune, India.

📝 License
Distributed under the MIT License. See LICENSE for more information.
