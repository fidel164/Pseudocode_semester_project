This section provides practical, task-focused instructions for performing key operations in the drone-based plant disease workflow.

## How to Load Drone Image Data
To load drone imagery into the workflow:

1. Ensure your files include metadata (sensor type, band count, etc.).
2. Provide the file path or database link to `load_drone_data()`.
3. The function will validate the source and return image data for further processing.


## How to Classify Drone Images (RGB vs. Multispectral)
Classification depends on sensor metadata:
Make sure you are working with multispectral sensors.

- RGB: 3 bands
- Multispectral: 4–5+ bands (Red-edge, NIR, etc.)

Use:

```python
classify_images(input_files)

## How to Compute NDVI or Other Vegetation Indices
Vegetation indices quantify plant stress signals caused by diseases.

To compute NDVI:

1. Run the workflow up to Step 4 (orthomosaic creation).
2. Ensure you have both **Red** and **NIR** calibrated band paths.
3. Call `calculate_VI()` to generate an NDVI raster.


