# workflow/step4_vi_qgis.py

from pathlib import Path
from typing import Union, Dict


def qgis_vi_checkpoint(output_folder: Union[str, Path]) -> Dict[str, Path]:
    """
    Step 4: QGIS vegetation index (VI) checkpoint.

    This step does NOT compute vegetation indices.
    QGIS is a external software to generate Vegetation Indices from Pix4D calibrated images (orthomosaics).

    Expected user workflow in QGIS:

      1. Load data
         - Open QGIS.
         - Add your multispectral raster files (e.g., drone orthomosaics or
           calibrated Pix4D band GeoTIFFs) that contain the bands needed
           for each VI (BLUE, RED, NIR, GREEN, RED_EDGE, etc.).

      2. Open Raster Calculator
         - Go to: Processing → Toolbox.
         - Search for “Raster Calculator”.
         - Double-click “Raster Calculator” to open it.

      3. Build vegetation index expressions
         - In Raster Calculator, select the bands needed for expressions like:
             NDVI  = (NIR - RED) / (NIR + RED)
             GNDVI = (NIR - GREEN) / (NIR + GREEN)
             NDRE  = (NIR - RE) / (NIR + RE)
         - Select the appropriate input bands from your raster layers.

      4. Export each VI
         - Set the output layer (file) in Raster Calculator.
         - Choose GeoTIFF format and a clear name, e.g.:
             NDVI.tif, GNDVI.tif, NDRE.tif
         - Save them into the chosen output folder.

      5. Verify outputs
         - Ensure the VI GeoTIFFs are georeferenced and stored in the
           same output folder that this Python step will scan.
    """
    output_folder = Path(output_folder).resolve()

    print("\n=== STEP 4: Vegetation Index Generation in QGIS (MANUAL STEP) ===")
    print("Use QGIS to calculate vegetation indices from Pix4D calibrated bands.\n")
    print("Place the exported VI GeoTIFFs in this folder:")
    print(f"  {output_folder}\n")

    print("Detailed actions in QGIS:")
    print("  1) Load Data:")
    print("     - Open QGIS.")
    print("     - Add your multispectral raster files (drone orthomosaics or")
    print("       calibrated band GeoTIFFs) with RED, NIR, GREEN, RED_EDGE, etc.")
    print("  2) Open Raster Calculator:")
    print("     - Go to Processing → Toolbox.")
    print("     - Search for 'Raster Calculator' and open it.")
    print("  3) Build VI expressions in Raster Calculator, e.g.:")
    print("     - NDVI  = (NIR - RED) / (NIR + RED)")
    print("     - GNDVI = (NIR - GREEN) / (NIR + GREEN)")
    print("     - NDRE  = (NIR - RE) / (NIR + RE)")
    print("  4) Export each VI as a GeoTIFF into the folder above,")
    print("     with clear names like NDVI.tif, GNDVI.tif, NDRE.tif.\n")

    input("Press ENTER when all VI GeoTIFFs are exported to this folder...\n")

    # --- DEBUG: show what Python actually sees in that folder ---
    print("DEBUG: Listing contents of output folder:")
    if not output_folder.exists():
        print("  (Folder does NOT exist!)")
    else:
        for item in output_folder.iterdir():
            print(f"  - {item.name}")
    print()

    # Detect GeoTIFF vegetation index rasters
    vi_dict: Dict[str, Path] = {}
    for item in output_folder.iterdir():
        if item.is_file() and item.suffix.lower() in (".tif", ".tiff"):
            stem_lower = item.stem.lower()
            if "ndvi" in stem_lower:
                vi_dict[item.stem.upper()] = item

    if not vi_dict:
        print(
            "WARNING: No GeoTIFF VI files found. "
            "Did you export them to the correct folder?"
        )
    else:
        print("Detected vegetation index files:")
        for name, path in vi_dict.items():
            print(f"  {name}: {path}")

    return vi_dict
