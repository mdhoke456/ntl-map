import rioxarray as rxr
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats
import folium

# --- Paths (relative) ---
RASTER = "data/viirs.tif"
WARDS = "data/Pune.geojson"
OUTPUT_HTML = "ntl_dec2025_map.html"

# --- Load data ---
ntl = rxr.open_rasterio(RASTER, masked=True)
wards = gpd.read_file(WARDS)

ntl = ntl.rio.write_crs("EPSG:4326")

# --- Zonal statistics ---
stats = zonal_stats(
    wards,
    RASTER,
    stats=["mean"],
    nodata=0
)

wards["ntl_mean"] = [s["mean"] for s in stats]

wards["ntl_class"] = pd.qcut(
    wards["ntl_mean"],
    q=4,
    labels=["Low", "Medium", "High", "Very High"]
)

# --- Folium map ---
m = folium.Map(
    location=[18.55, 73.97],
    zoom_start=10,
    tiles="CartoDB dark_matter"
)

def style_fn(feature):
    colors = {
        "Low": "#2c7bb6",
        "Medium": "#abd9e9",
        "High": "#fdae61",
        "Very High": "#d7191c"
    }
    cls = feature["properties"]["ntl_class"]
    return {
        "fillColor": colors.get(cls, "#cccccc"),
        "color": "black",
        "weight": 0.4,
        "fillOpacity": 0.7
    }

folium.GeoJson(
    wards,
    style_function=style_fn,
    tooltip=folium.GeoJsonTooltip(
        fields=["NAME_3", "ntl_mean"],
        aliases=["Ward", "Mean NTL (Dec 2025)"]
    )
).add_to(m)

m.save(OUTPUT_HTML)
print(f"Map saved to {OUTPUT_HTML}")

