import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Define file paths
processed_dir = "data/processed/"  # <-- FIXED DIRECTORY PATH
valid_files = ["MODIS_NDVI.tif", "MODIS_NDVI_WGS84.tif", "MODIS_NDVI_500x500.tif"]

# Find an available file
ndvi_file = None
for file in valid_files:
    file_path = os.path.join(processed_dir, file)
    if os.path.exists(file_path):
        ndvi_file = file_path
        break

if ndvi_file is None:
    print(f"❌ No valid NDVI file found in {processed_dir}. Please check the file names.")
    print("📂 Checking available files in processed directory:")
    print(os.listdir(processed_dir))
    exit()

print(f"✅ Using NDVI file: {ndvi_file}")

# Open raster file
with rasterio.open(ndvi_file) as src:
    ndvi = src.read(1).astype(float)
    ndvi = ndvi * 0.0001  # Apply MODIS scale factor

# Plot NDVI
plt.figure(figsize=(10, 6))
plt.imshow(ndvi, cmap="YlGn", vmin=-1, vmax=1)  # NDVI range is -1 to 1
plt.colorbar(label="NDVI (Scaled)")
plt.title("MODIS NDVI (Scaled)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.show()
