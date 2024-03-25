import os
import json
import shutil

# Function to get key names from a JSON file
def get_key_names(json_file):
    with open(json_file, 'r') as f:
        try:
            data = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error decoding JSON in file {json_file}: {e}")
            return None

        if isinstance(data, list):
            # If JSON is an array, take keys from the first object
            if data:
                return set(data[0].keys())
            else:
                return set()
        else:
            # If JSON is an object, take keys directly
            return set(data.keys())

# Function to organize JSON files into two directories
def organize_json_files(folder_path, same_keys_dir, different_keys_dir):
    # Create directories if they don't exist
    os.makedirs(same_keys_dir, exist_ok=True)
    os.makedirs(different_keys_dir, exist_ok=True)

    # Set to store key names from the first JSON file
    first_key_names = None

    # Iterate through each file in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.json'):
            key_names = get_key_names(file_path)
            if key_names is not None:
                # Store key names from the first JSON file
                if first_key_names is None:
                    first_key_names = key_names
                # Check if the key names are the same as the first JSON file
                if key_names == first_key_names:
                    shutil.copy(file_path, same_keys_dir)
                else:
                    shutil.copy(file_path, different_keys_dir)

# Example usage
folder_path = r'C:\Users\purru\Desktop\PricingTransparencyInHealth-ProcedurePriceMatch\JSON-FILES WITH ZIPCODE'
same_keys_dir = 'same_keys_json_files'
different_keys_dir = 'different_keys_json_files'

organize_json_files(folder_path, same_keys_dir, different_keys_dir)
