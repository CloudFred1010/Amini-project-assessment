import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling

def reproject_raster(input_raster, output_raster):
    with rasterio.open(input_raster) as src:
        transform, width, height = calculate_default_transform(
            src.crs, "EPSG:4326", src.width, src.height, *src.bounds
        )
        kwargs = src.meta.copy()
        kwargs.update({
            "crs": "EPSG:4326",
            "transform": transform,
            "width": width,
            "height": height
        })

        with rasterio.open(output_raster, "w", **kwargs) as dst:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dst, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs="EPSG:4326",
                    resampling=Resampling.nearest
                )

# Apply reprojection
reproject_raster("climate_risk_analysis/data/raw/MODIS_NDVI.tif", "climate_risk_analysis/data/processed/MODIS_NDVI_WGS84.tif")

print("✅ Reprojection completed successfully!")
