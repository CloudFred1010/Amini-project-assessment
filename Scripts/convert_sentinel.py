import os
import rasterio
from rasterio.plot import show
from glob import glob

# Define input directory (where SAFE files are stored)
input_dir = "data/satellite_data/"
output_dir = "data/processed/"

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Process each extracted Sentinel-1 SAFE folder
for safe_folder in os.listdir(input_dir):
    if safe_folder.endswith(".SAFE"):
        measurement_dir = os.path.join(input_dir, safe_folder, "measurement")
        for tiff_file in glob(f"{measurement_dir}/*.tiff"):
            print(f"Processing {tiff_file}...")

            # Open TIFF file
            with rasterio.open(tiff_file) as src:
                # Define output path
                output_tiff = os.path.join(output_dir, os.path.basename(tiff_file).replace(".tiff", "_processed.tif"))
                profile = src.profile
                profile.update(dtype=rasterio.float32)

                # Save as new GeoTIFF
                with rasterio.open(output_tiff, "w", **profile) as dest:
                    dest.write(src.read(1), 1)
                
                print(f"✅ Saved: {output_tiff}")
