# workflow/step3_pix4d.py

from pathlib import Path
from typing import Union, Optional


def pix4d_checkpoint(
    image_folder: Union[str, Path], project_note: Optional[str] = None
) -> None:
    """
    Step 3: Manual Pix4D checkpoint.

    This step does NOT run Pix4D itself. It:
      - Shows which folder to use in Pix4D
      - Optionally prints a note/label
      - Pauses the workflow until the user presses ENTER

    Core Pix4D processing workflow (summary):
      1. Create project & import images.
      2. Set project name, save location, and CRS.
      3. For Calibration, import GCPs and mark them in images.
      4. Run Initial Processing (keypoints, camera optimization, ATPs).
      5. Run Point Cloud & Mesh (dense cloud + 3D mesh).
      6. Run DSM, Orthomosaic & Index (georeferenced outputs).
      7. Export deliverables (DSM, orthomosaic, point cloud, mesh, etc.).
    """
    folder = Path(image_folder).resolve()
    print("\n=== STEP 3: Pix4D Orthomosaic Creation (MANUAL STEP) ===")
    print(f"Use this image folder in Pix4D:\n  {folder}")

    if project_note:
        print(f"Project note: {project_note}")

    print("\nCore Pix4D workflow:")
    print("  1) Create project & import images")
    print("  2) Set project name, save location, CRS")
    print("  3) Calibration, import GCPs and mark them")
    print("  4) Run Initial Processing")
    print("  5) Run Point Cloud & Mesh")
    print("  6) Run DSM, Orthomosaic & Index")
    print("  7) Export DSM / orthomosaic / point cloud / mesh\n")

    print("Instructions for this project:")
    print("  - Use the folder above as input images.")
    print(
        "  - Generate at least: calibrated orthomosaic per each sensor band (e.g. blue, green, nir, red_edge, red)."
    )
    print(
        "  - Note the output folder and filenames will contains images in format GeoTIFFs for the next Python step.\n"
    )

    input("When Pix4D has finished and outputs are ready, press ENTER to continue...\n")
