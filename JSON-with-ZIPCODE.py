import os
import json
from tqdm import tqdm
import shutil

# Base directory where the JSON files are initially located
base_dir = 'C:/Users/purru/Desktop/PricingTransparencyInHealth-ProcedurePriceMatch/Hospital Price Transparency Data'
# New directory to store JSON files
json_files_dir = 'JSON-FILES WITH ZIPCODE'

# Ensure json-files directory exists
os.makedirs(json_files_dir, exist_ok=True)


def find_json_files(directory):
    """Generator function to find all JSON files within the directory and its subdirectories."""
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                yield os.path.join(root, file)


def copy_json_to_folder(file_path):
    """Copy the JSON file to the specified folder."""
    # Extract ZIP code from folder name
    zip_code = None
    current_dir = os.path.dirname(file_path)
    while True:
        current_dir, folder_name = os.path.split(current_dir)
        if folder_name.isnumeric() and len(folder_name) == 5:  # Check if it's a ZIP code
            zip_code = folder_name
            break
        elif current_dir == base_dir:  # Stop if reached the base directory
            break

    if zip_code:
        # Generate new filename with ZIP code
        new_filename = f"{zip_code}_{os.path.basename(file_path)}"
        # Generate new path in json-files directory
        new_path = os.path.join(json_files_dir, new_filename)
        # Copy JSON file to the new path
        shutil.copy(file_path, new_path)


def main():
    json_files = list(find_json_files(base_dir))
    progress_bar = tqdm(total=len(json_files), desc="Copying JSON files", unit="file")

    for file_path in json_files:
        copy_json_to_folder(file_path)
        progress_bar.update(1)

    progress_bar.close()


if __name__ == "__main__":
    main()
