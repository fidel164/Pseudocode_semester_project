# run_workflow.py

from workflow.step1_load import load_drone_data


def main():
    print("=== STEP 1: Loading drone images ===")

    # Replace this with your real path
    folder = "/Users/fideljimenez/Library/CloudStorage/OneDrive-MichiganStateUniversity/Michigan State University/Courses/Fall 2025/CMSE_890_Computational_Workflow/Drone images"

    images = load_drone_data(folder)
    print("Loaded images:")
    for img in images:
        print(" -", img["path"])

    print("Workflow Step 1 completed!")


if __name__ == "__main__":
    main()
