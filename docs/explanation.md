This section explains the scientific principles, remote sensing methods, and analytical reasoning behind the workflow.

## Multispectral Drone Imagery
Multispectral sensors (e.g., RedEdge, Sequoia) capture reflectance in several spectral bands.  
Plants reflect and absorb light differently depending on chlorophyll content, water stress, and disease presence.

Key bands:

- Red
- Green
- Blue
- Near-Infrared (NIR)
- Red-edge
- Thermal (sometimes) 

Healthy plants → high NIR reflectance  
Stressed/diseased plants → lower NIR, altered red-edge response

---

## NDVI and Plant Health
NDVI = (NIR – Red) / (NIR + Red)

NDVI rises with:

- chlorophyll density  
- leaf area index (LAI)  
- photosynthetic activity  

## How Pix4D Orthomosaics Work
Pix4D uses photogrammetry to convert overlapping drone images into:

- georeferenced mosaics  
- reflectance-calibrated band rasters  
- radiometrically corrected values suitable for analysis  

Your workflow assumes Pix4D (or similar software) has already produced calibrated **Red** and **NIR** orthomosaics.

## Correlating Drone Data With Disease Severity
After NDVI and plot features are computed:

- disease severity scores (field ratings, AUDPC, infection percentages)
- are statistically compared to drone-derived metrics

This determines which indices or metrics best predict disease levels.

The workflow uses an R-based correlation tool for flexibility in:

- Pearson, Spearman, Kendall correlations  
- mixed models  
- ANOVA-based comparisons  