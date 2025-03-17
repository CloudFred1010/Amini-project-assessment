import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Define the processed data directory
processed_dir = "data/processed/"
plots_dir = "data/plots"

# Ensure the plots directory exists
os.makedirs(plots_dir, exist_ok=True)

# Get all SMAP soil moisture .tif files
tif_files = [f for f in os.listdir(processed_dir) if f.startswith("SMAP") and f.endswith(".tif")]

if not tif_files:
    print("❌ No SMAP Soil Moisture TIFF files found.")
    exit()

for tif_file in tif_files:
    tif_path = os.path.join(processed_dir, tif_file)

    with rasterio.open(tif_path) as src:
        img = src.read(1).astype(float)

        # Handle NoData values
        if src.nodata is not None:
            img[img == src.nodata] = np.nan  # Replace -9999 with NaN

        # Filter out NoData values for statistics
        valid_data = img[~np.isnan(img)]
        if valid_data.size > 0:
            min_val, max_val, mean_val = np.nanmin(valid_data), np.nanmax(valid_data), np.nanmean(valid_data)
            print(f"✅ {tif_file}: Min: {min_val:.4f}, Max: {max_val:.4f}, Mean: {mean_val:.4f}")
        else:
            print(f"⚠ {tif_file}: No valid data available.")

        # Define spatial extent
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

        # Plot the raster and save it
        plt.figure(figsize=(8, 6))
        plt.imshow(img, cmap="viridis", extent=extent, aspect='auto')
        plt.colorbar(label="Soil Moisture")
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"SMAP Soil Moisture: {tif_file}")

        # Save plot
        plot_path = os.path.join(plots_dir, f"{tif_file.replace('.tif', '.png')}")
        plt.savefig(plot_path, dpi=300, bbox_inches="tight")
        print(f"📊 Saved plot: {plot_path}")

        plt.close()  # Close the figure to free memory

