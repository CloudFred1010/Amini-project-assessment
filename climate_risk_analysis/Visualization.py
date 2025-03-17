import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Define the processed data directory
processed_dir = "data/processed/"

# Get all .tif files
tif_files = [f for f in os.listdir(processed_dir) if f.endswith(".tif")]

if not tif_files:
    print("❌ No TIFF files found in processed directory.")
    exit()

for tif_file in tif_files:
    tif_path = os.path.join(processed_dir, tif_file)

    with rasterio.open(tif_path) as src:
        img = src.read(1)  # Read the first (and only) band

        # Replace NoData values with NaN
        if src.nodata is not None:
            img = np.where(img == src.nodata, np.nan, img)

        # Print statistics
        min_val, max_val, mean_val = np.nanmin(img), np.nanmax(img), np.nanmean(img)
        print(f"✅ {tif_file}: Min: {min_val}, Max: {max_val}, Mean: {mean_val}")

        # Define spatial extent for georeferencing
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

        # Plot the raster
        plt.figure(figsize=(8, 6))
        plt.imshow(img, cmap="viridis", extent=extent, aspect='auto')
        plt.colorbar(label="Soil Moisture")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"Processed SMAP Soil Moisture Data: {tif_file}")
        plt.show()

