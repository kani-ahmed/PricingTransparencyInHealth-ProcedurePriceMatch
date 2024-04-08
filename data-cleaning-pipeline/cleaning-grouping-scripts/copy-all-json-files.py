import os
from tqdm import tqdm
import shutil  # Import the shutil module

# Base directory where the JSON files are initially located
base_dir = '../../Hospital Price Transparency Data'
# New directory to store JSON files
json_files_dir = '../../data-cleaning-pipeline-generated-data/json-files'

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
    new_path = os.path.join(json_files_dir, os.path.basename(file_path))
    # Ensure there is no filename conflict
    if os.path.exists(new_path):
        base, extension = os.path.splitext(os.path.basename(file_path))
        i = 1
        while os.path.exists(new_path):
            new_filename = f"{base}_{i}{extension}"
            new_path = os.path.join(json_files_dir, new_filename)
            i += 1
    shutil.copy(file_path, new_path)  # Copy file


def main():
    json_files = list(find_json_files(base_dir))
    progress_bar = tqdm(total=len(json_files), desc="Copying JSON files", unit="file")

    for file_path in json_files:
        copy_json_to_folder(file_path)
        progress_bar.update(1)

    progress_bar.close()


if __name__ == "__main__":
    main()
