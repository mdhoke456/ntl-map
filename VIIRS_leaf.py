import rioxarray as rxr
import geopandas as gpd
import pandas as pd
from rasterstats import zonal_stats
import folium

# --- Paths (relative) ---
RASTER = "data/viirs.tif"
WARDS = "data/Pune.geojson"
OUTPUT_HTML = "index.html"

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

title_html = '''
             <h3 align="center" style="font-size:20px; color:white; 
             position:fixed; top:10px; left:50%; transform:translateX(-50%); 
             z-index:9999; background-color:rgba(0,0,0,0.6); padding:10px; 
             border-radius:10px; font-family: sans-serif;">
             Pune Nightlight Intensity (Dec 2025)
             </h3>
             '''

legend_html = '''
     <div style="position: fixed; 
     bottom: 30px; left: 30px; width: 160px; height: auto; 
     background-color: rgba(255, 255, 255, 0.9); border:2px solid grey; 
     z-index:9999; font-size:14px; padding: 10px; border-radius: 8px;
     font-family: sans-serif; line-height: 1.6;">
     <b>NTL Class</b><br>
     <i style="background:#d7191c; width:12px; height:12px; display:inline-block; border:1px solid #000;"></i> Very High<br>
     <i style="background:#fdae61; width:12px; height:12px; display:inline-block; border:1px solid #000;"></i> High<br>
     <i style="background:#abd9e9; width:12px; height:12px; display:inline-block; border:1px solid #000;"></i> Medium<br>
     <i style="background:#2c7bb6; width:12px; height:12px; display:inline-block; border:1px solid #000;"></i> Low
     </div>
     '''

m.get_root().html.add_child(folium.Element(title_html))
m.get_root().html.add_child(folium.Element(legend_html))

m.save(OUTPUT_HTML)
print(f"Map saved to {OUTPUT_HTML}")

