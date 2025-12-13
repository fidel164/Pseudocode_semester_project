from pathlib import Path
from typing import Iterable, List, Dict, Union


def load_drone_data(source: Union[str, Path, Iterable[Union[str, Path]]]) -> List[Dict]:
    """Load raw drone image *paths* from a file, directory, or list."""
    if isinstance(source, (str, Path)):
        source = Path(source)
        if source.is_dir():
            files = sorted(
                list(source.glob("*.tif"))
                + list(source.glob("*.tiff"))
                + list(source.glob("*.jpg"))
                + list(source.glob("*.jpeg"))
                + list(source.glob("*.PNG"))
            )
            if not files:
                raise FileNotFoundError(f"No image files found in directory: {source}")
        elif source.is_file():
            files = [source]
        else:
            raise FileNotFoundError(f"No such file or directory: {source}")
    else:
        files = [Path(p) for p in source]
        missing = [f for f in files if not f.exists()]
        if missing:
            missing_str = ", ".join(str(f) for f in missing)
            raise FileNotFoundError(f"The following files do not exist: {missing_str}")

    images = []
    for f in files:
        images.append(
            {
                "path": f,
                "sensor_type": None,
                "bands": None,
            }
        )

    return images
