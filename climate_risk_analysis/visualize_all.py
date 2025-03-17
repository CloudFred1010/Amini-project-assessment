import subprocess

print("🟢 Running NDVI Visualization...")
subprocess.run(["python", "visualize_ndvi.py"])

print("🟢 Running Soil Moisture Visualization...")
subprocess.run(["python", "visualize_soil_moisture.py"])
