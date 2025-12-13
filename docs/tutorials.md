# NDVI Tutorial: Understanding and computing NDVI from drone imagery

NDVI (Normalized Difference Vegetation Index) is one of the most widely used vegetation indices in remote sensing. It is especially useful for monitoring plant health, crop stress, and disease progression.

This tutorial explains:

1. What NDVI is
2. Why it matters
3. How your workflow computes NDVI using drone multispectral imagery
4. What the output looks like and how to interpret it

##1. What Is NDVI?
NDVI is a simple mathematical ratio used to quantify vegetation health. It compares how much near-infrared (NIR) light a plant reflects versus red light it absorbs.
Healthy plants strongly reflect NIR and absorb red light. Stressed or diseased plants show reduced NIR reflectance and increased red reflectance.

##2. NDVI Formula
The formula is:
NDVI= (NIR−Red)/(NIR+Red)
Values range from –1 to +1:

NDVI Value	Meaning
> 0.6	Dense, healthy vegetation
0.2 – 0.6	Moderate vegetation or stressed
0 – 0.2	Bare soil, sparse vegetation
< 0	Water, shadows, clouds

##3. NDVI in Your Workflow
Python pseudocode computes NDVI 
Step by step
Step 1 — Load the red band
red_ds = gdal.Open(red_band)
red_band_data = red_ds.GetRasterBand(1).ReadAsArray().astype(float)

Step 2 — Load the NIR band
nir_ds = gdal.Open(nir_band)
nir_band_data = nir_ds.GetRasterBand(1).ReadAsArray().astype(float)

Step 3 — Compute NDVI
ndvi = (nir_band_data - red_band_data) / (nir_band_data + red_band_data)

Step 4 — Return the NDVI raster
The output is an NDVI array, where each pixel represents vegetation health.

##4. Interpreting NDVI Results

Once NDVI is computed, you can visualize it:

*Bright green/yellow = healthy vegetation
*Orange/red = stressed or diseased plants
*Dark areas = soil, water, shadows
*Higher NDVI → higher chlorophyll content → healthier plants.