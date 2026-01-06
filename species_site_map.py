import pandas as pd
import folium
import utm
import os

# Load the FWIN Excel data
df = pd.read_excel("C:\\Users\\jnhernandez\\Documents\\Bio 2\\Data 2025\\Starvation\\SV.GN.2025.FWIN.xlsx")

# Define species codes to generate maps for
species_list = ["WAE", "SMB", "RBT", "YP", "BNT"]
output_dir = "figures"

# Ensure output folders exist
for species in species_list:
    folder = os.path.join(output_dir, species.lower().replace(" ", "_"))
    os.makedirs(folder, exist_ok=True)

# Convert UTM to lat/lon
def convert_utm_to_latlon(easting, northing, zone=12):
    try:
        lat, lon = utm.to_latlon(easting, northing, zone, 'N')
        return lat, lon
    except Exception:
        return None, None

# Loop through each species and generate a site map
for spp in species_list:
    subset = df[df["SPP"] == spp]
    if subset.empty:
        continue

    first_lat, first_lon = convert_utm_to_latlon(subset.iloc[0]["UTM_E"], subset.iloc[0]["UTM_N"])
    m = folium.Map(location=[first_lat, first_lon], zoom_start=12)

    for _, row in subset.iterrows():
        lat, lon = convert_utm_to_latlon(row["UTM_E"], row["UTM_N"])
        if lat and lon:
            folium.CircleMarker(
                location=(lat, lon),
                radius=5,
                color="blue",
                fill=True,
                fill_opacity=0.7,
                popup=f"{spp} Net Location"
            ).add_to(m)

    output_path = os.path.join(output_dir, spp.lower().replace(" ", "_"), "site_map.html")
    m.save(output_path)

print("Species maps saved successfully!")
