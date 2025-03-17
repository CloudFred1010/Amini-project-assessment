import rasterio
from rasterio.enums import Resampling

def resample_raster(input_raster, output_raster, target_shape=(500, 500)):
    with rasterio.open(input_raster) as src:
        transform = src.transform * src.transform.scale(
            (src.width / target_shape[1]),
            (src.height / target_shape[0])
        )

        resampled_array = src.read(
            out_shape=(src.count, *target_shape),
            resampling=Resampling.bilinear
        )

        kwargs = src.meta.copy()
        kwargs.update({
            "height": target_shape[0],
            "width": target_shape[1],
            "transform": transform
        })

        with rasterio.open(output_raster, "w", **kwargs) as dst:
            dst.write(resampled_array)

# Apply resampling
resample_raster(
    "climate_risk_analysis/data/processed/MODIS_NDVI_WGS84.tif", 
    "climate_risk_analysis/data/processed/MODIS_NDVI_500x500.tif"
)

print("✅ Resampling completed successfully!")
