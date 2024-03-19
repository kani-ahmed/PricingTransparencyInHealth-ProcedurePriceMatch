import os
import json


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


def main(folder_path):
    files = os.listdir(folder_path)
    same_key_names = {}
    different_key_names = {}

    # Iterate through each file
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.json'):
            key_names = get_key_names(file_path)
            if key_names is not None:
                key_names_tuple = tuple(sorted(key_names))  # Convert set to sorted tuple for consistency
                if key_names_tuple in same_key_names:
                    same_key_names[key_names_tuple].append(file_name)
                else:
                    # Add the set of key names to the dictionary
                    same_key_names[key_names_tuple] = [file_name]

    # Print files with same key names
    print("\nFiles with same key names:")
    for key_names, filenames in same_key_names.items():
        print(f"Key names: {key_names}, Files: {filenames}")

    # Print files with different key names
    print("\nFiles with different key names:")
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.endswith('.json'):
            key_names = get_key_names(file_path)
            if key_names is not None:
                key_names_tuple = tuple(sorted(key_names))  # Convert set to sorted tuple for consistency
                if key_names_tuple not in same_key_names:
                    print(f"File {file_name} has different key names: {key_names}")


# Example usage
folder_path = r'C:\Users\purru\Desktop\PricingTransparencyInHealth-ProcedurePriceMatch\json-files'
main(folder_path)
