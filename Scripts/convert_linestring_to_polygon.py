from osgeo import ogr

# Set correct file paths
input_shapefile = "/mnt/c/Users/wilfr/Amini-project-assessment/data/admin_boundaries/elgeyo_marakwet_admin1_fixed.shp"
output_shapefile = "/mnt/c/Users/wilfr/Amini-project-assessment/data/admin_boundaries/elgeyo_marakwet_admin1_polygon_fixed.shp"

# Open the original shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")
source_ds = driver.Open(input_shapefile, 0)  # Open in read-only mode
if source_ds is None:
    raise RuntimeError(f"Failed to open source shapefile: {input_shapefile}")

source_layer = source_ds.GetLayer()

# Check the feature count
feature_count = source_layer.GetFeatureCount()
print(f"Number of features in source file: {feature_count}")

if feature_count == 0:
    raise RuntimeError("No features found in source shapefile!")

# Create a new shapefile for the polygon
out_driver = ogr.GetDriverByName("ESRI Shapefile")
out_ds = out_driver.CreateDataSource(output_shapefile)
out_layer = out_ds.CreateLayer("elgeyo_marakwet_admin1_polygon_fixed", source_layer.GetSpatialRef(), ogr.wkbPolygon)

# Copy attributes from the original file
layer_defn = source_layer.GetLayerDefn()
for i in range(layer_defn.GetFieldCount()):
    out_layer.CreateField(layer_defn.GetFieldDefn(i))

# Convert LineString to Polygon
polygon_count = 0
for feature in source_layer:
    geom = feature.GetGeometryRef()
    if geom and geom.GetGeometryType() == ogr.wkbLineString:
        # Convert LineString to a LinearRing
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for i in range(geom.GetPointCount()):
            ring.AddPoint(*geom.GetPoint(i))

        # Ensure the ring is closed
        if ring.GetPoint(0) != ring.GetPoint(ring.GetPointCount() - 1):
            ring.AddPoint(*ring.GetPoint(0))  # Close the ring manually

        # Create a polygon from the ring
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        # Create a new feature with the polygon
        new_feature = ogr.Feature(out_layer.GetLayerDefn())
        new_feature.SetGeometry(poly)

        # Copy attributes
        for i in range(layer_defn.GetFieldCount()):
            new_feature.SetField(i, feature.GetField(i))

        # Add the new polygon feature
        out_layer.CreateFeature(new_feature)
        new_feature = None  # Free memory

        polygon_count += 1

print(f"Successfully created {polygon_count} polygons.")

# Cleanup
source_ds = None
out_ds = None
