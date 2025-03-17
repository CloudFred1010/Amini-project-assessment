import os
import rasterio
import geopandas as gpd
from rasterio.mask import mask

# Define paths
boundary_path = "data/admin_boundaries/elgeyo_marakwet_admin3.shp"
input_dir = "data/processed/"
output_dir = "data/clipped/"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Load the Elgeyo Marakwet Admin 3 boundaries
admin_boundaries = gpd.read_file(boundary_path)

# Process each processed GeoTIFF
for tiff_file in os.listdir(input_dir):
    if tiff_file.endswith(".tif"):
        input_path = os.path.join(input_dir, tiff_file)
        print(f"Clipping {input_path}...")

        with rasterio.open(input_path) as src:
            out_image, out_transform = mask(src, admin_boundaries.geometry, crop=True)
            out_meta = src.meta.copy()
            out_meta.update({"driver": "GTiff", "height": out_image.shape[1], "width": out_image.shape[2], "transform": out_transform})

        # Save clipped raster
        output_file = os.path.join(output_dir, f"clipped_{tiff_file}")
        with rasterio.open(output_file, "w", **out_meta) as dest:
            dest.write(out_image)

        print(f"✅ Saved clipped raster: {output_file}")
