import h5py
import rasterio
import numpy as np
import os

# Define input and output directories
input_dir = "data/raw/"
output_dir = "data/processed/"
os.makedirs(output_dir, exist_ok=True)

# Dataset key for extraction
dataset_key = "Soil_Moisture_Retrieval_Data/soil_moisture"

for filename in os.listdir(input_dir):
    if filename.endswith(".h5"):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename.replace(".h5", ".tif"))

        try:
            with h5py.File(input_file, "r") as h5f:
                if dataset_key in h5f:
                    dataset = h5f[dataset_key][:]
                    
                    # 🔹 Ensure dataset is at least 2D
                    if dataset.ndim == 1:
                        dataset = np.expand_dims(dataset, axis=0)  # Convert to (1, N)
                    
                    height, width = dataset.shape
                    
                    # 🔹 Replace NoData values (-9999.0) with NaN
                    dataset = np.where(dataset == -9999.0, np.nan, dataset)

                    # 🔹 Define correct georeferencing transform
                    transform = rasterio.transform.from_origin(
                        -180, 90,  # Adjust top-left corner if necessary
                        0.25, 0.25  # Pixel size (adjust for dataset resolution)
                    )

                    with rasterio.open(
                        output_file,
                        "w",
                        driver="GTiff",
                        height=height,
                        width=width,
                        count=1,
                        dtype=np.float32,
                        crs="EPSG:4326",
                        transform=transform,
                        nodata=np.nan  # Preserve NaN as NoData
                    ) as dst:
                        dst.write(dataset, 1)

                    print(f"✅ Successfully converted: {input_file} → {output_file} ({width} x {height})")
                else:
                    print(f"⚠ Dataset key '{dataset_key}' not found in {input_file}. Skipping...")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

print("🎯 Conversion process completed!")
