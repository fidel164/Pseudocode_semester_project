# run_workflow.py

from workflow.step1_load import load_drone_data
from workflow.step2_filter import filter_and_classify
from workflow.step3_pix4d import pix4d_checkpoint
from workflow.step4_vi_qgis import qgis_vi_checkpoint


def main():
    print("=== STEP 1: Loading drone images ===")

    # Replace this with your real path
    folder = "/Users/fideljimenez/Library/CloudStorage/OneDrive-MichiganStateUniversity/Michigan State University/Courses/Fall 2025/CMSE_890_Computational_Workflow/Drone images"

    images = load_drone_data(folder)
    print("Loaded images:")
    for img in images:
        print(" -", img["path"])

    print("Workflow Step 1 completed!")

    print("=== STEP 2: Filtering & Classifying ===")
    filtered = filter_and_classify(images)

    print("Classification results:")
    for img in filtered:
        print(f"{img['path'].name}: {img['sensor_type']}")

    print("Workflow Step 2 completed!")

    print("=== STEP 3: Pix4D checkpoint (manual step) ===")
    pix4d_checkpoint(folder, project_note="My drone experiment")
    print("Workflow Step 3 completed (returned from Pix4D checkpoint).")

    print("=== STEP 4: QGIS VI checkpoint (manual step) ===")
    vi_output_folder = "/Users/fideljimenez/Library/CloudStorage/OneDrive-MichiganStateUniversity/Michigan State University/Courses/Fall 2025/CMSE_890_Computational_Workflow/Drone images/VI_outputs"

    vi_files = qgis_vi_checkpoint(vi_output_folder)

    print("Workflow Step 4 completed. Detected vegetation indices:")
    for name, path in vi_files.items():
        print(f"  {name}: {path}")


if __name__ == "__main__":
    main()
