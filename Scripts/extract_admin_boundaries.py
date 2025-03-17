import geopandas as gpd

# Load the Kenya admin shapefile
shapefile_path = "data/gadm41_KEN_shp/gadm41_KEN_3.shp"
kenya_admin = gpd.read_file(shapefile_path)

# Extract Elgeyo Marakwet County (Admin 1)
elgeyo_marakwet = kenya_admin[kenya_admin["NAME_1"] == "Elgeyo Marakwet"]

# Extract Admin 3 subdivisions within the county
admin_3_subdivisions = elgeyo_marakwet[elgeyo_marakwet["NAME_3"].notna()]

# Save the extracted shapefiles
elgeyo_marakwet.to_file("data/elgeyo_marakwet_admin1.shp")
admin_3_subdivisions.to_file("data/elgeyo_marakwet_admin3.shp")

print("✅ Admin 3 boundaries extracted successfully!")
