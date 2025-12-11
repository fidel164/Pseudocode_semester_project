# workflow/step2_filter.py

from pathlib import Path
from typing import List, Dict


def classify_image_by_filename(path: Path) -> str:
    """
    Classify an image as 'rgb' or 'multispectral' based on filename hints.

    This is a simple placeholder classification:
      - Files containing 'RGB' or 'rgb' → RGB
      - Files containing 'blue', 'green', 'nir', 'red_edge', 'red' or 'ms' → multispectral
      - Otherwise default to 'unknown'
    """
    name = path.name.lower()

    if "rgb" in name:
        return "rgb"
    if any(
        x in name
        for x in ["blue", "green", "nir", "rededge", "red", "ms", "multispectral"]
    ):
        return "multispectral"

    return "unknown"


def filter_and_classify(images: List[Dict]) -> List[Dict]:
    """
    Filter invalid images and classify each into rgb / multispectral / unknown.
    """
    filtered = []

    for img in images:
        path = img["path"]

        # Skip non-files
        if not path.exists():
            continue

        # Classify image
        img_type = classify_image_by_filename(path)

        # Store result
        img["sensor_type"] = img_type
        filtered.append(img)

    return filtered
