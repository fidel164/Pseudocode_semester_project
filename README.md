Drone-imagery Workflow for Plant Disease Analysis
Overview

This project implements a modular and reproducible computational workflow to process drone-derived multispectral imagery and quantify the relationship between vegetation indices (NDVI) and plant disease severity at the plot level.

The workflow combines manual photogrammetry and GIS steps (Pix4D, QGIS) with automated Python processing, statistical analysis, and visualization.

This workflow was made following the dataflow diagram (DFDs) submitted at the beginning of the semester for the course CMSE 890-602: Reproducible Computational Workflows.

This final outputs include:

-cleaned NDVI rasters
-plot-level NDVI features
-correlation statistics
-plots of NDVI vs disease severity correlation

Workflow Structure
Manual Checkpoints

Some steps require external software and are documented as checkpoints rather than automated code. For instance:

Step 3 – Pix4D

-Orthomosaic creation
-Radiometric calibration
-Export per-band GeoTIFFs

Step 4 – QGIS

-NDVI calculation
-Export NDVI GeoTIFF

These steps are paused in the workflow and resumed once outputs are ready.

Automated Steps (Python) are unit tested using pytest.
Step                                   Output
Step 1	Load drone image paths	    -> metadata
Step 2	Filter & classify imagery   -> RGB / multispectral
Step 5	NDVI background removal	    -> ndvi_cleaned.tif
Step 6	Experimental plot detection	-> Plot bounding boxes
Step 7	Feature extraction	        -> features_step7.csv
Step 8	Correlation analysis	    -> correlations_step8.csv
Step 9	Visualization	            -> ndvi_vs_disease.png



Repository Structure
Pseudocode_semester_project/
├── workflow/
│   ├── step1_load.py
│   ├── step2_filter.py
│   ├── step3_pix4d.py
│   ├── step4_vi_qgis.py
│   ├── step5_background.py
│   ├── step6_plots.py
│   ├── step7_features.py
│   ├── step8_correlation.py
│   └── step9_plotting.py
├── tests/
│   ├── test_step5_background.py
│   ├── test_step6_plots.py
│   ├── test_step7_features.py
│   ├── test_step8_correlation.py
│   └── test_step9_plotting.py
├── DataStore/
│   ├── ndvi_cleaned.tif
│   ├── features_step7.csv
│   ├── disease_ratings.csv
│   ├── correlations_step8.csv
│   └── ndvi_vs_disease.png
├── run_workflow.py
└── README.md

Requirements:
-Python
-Python ≥ 3.9
-numpy
-pandas
-matplotlib
-pytest
-rasterio or GDAL (for GeoTIFF I/O)

Install dependencies with:
in bash terminal: python3 -m pip install numpy pandas matplotlib pytest rasterio

How to Run the Workflow
From the project root:
in bash terminal: python3 run_workflow.py

The script will:
1. Load drone imagery
2. Classify format of drone imagery
3. Checkpoint for Pix4D processing
4. Checkpoint for QGIS NDVI generation
5. Automatically clean NDVI
6. Automatically detect experimental plots
7. Automatically extract NDVI features per plot
8. Merge features with disease data
9. Compute correlations
10. Generate NDVI vs disease plots


Disease Data Input
To run correlation analysis, a disease severity file must exist:
DataStore/disease_ratings.csv
Required format
plot_id,disease_severity
plot_1,22
plot_2,55

Things to consider:
-Each row must correspond to a plot detected in Step 6.

Outputs
All outputs are written to the DataStore/ directory:
ndvi_cleaned.tif – NDVI raster with background removed
features_step7.csv – plot-level NDVI statistics
correlations_step8.csv – correlation coefficients
ndvi_vs_disease.png – scatter plot with regression line

Scientific Interpretation
The workflow is designed to evaluate relationships such as:
Higher NDVI or vegetation indices values are associated with lower disease severity, indicating healthier canopy conditions.

The modular structure allows easy extension to:
-multiple dates
-multiple locations
-treatment comparisons
-mixed-effects models
-integration with R (ggplot2, lme4)

Limitations:
-Manual Pix4D and QGIS steps are intentionally excluded from automation due to licensing and GUI requirements.

Notes
-All automated steps are tested independently to ensure correctness and reproducibility.
-The workflow is designed for scalability to real field experiments.

Author

Fidel E. Jiménez-Beitia
Ph.D. Student
Plant Pathology & Digital Agriculture