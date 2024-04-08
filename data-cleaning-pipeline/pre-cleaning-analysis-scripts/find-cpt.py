import os
import json


def search_cpt_in_json_files(parent_dir):
    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        # Convert the JSON data to a string to search for the keyword "CPT"
                        data_str = json.dumps(data)
                        if "Associated_Codes" in data_str:
                            print(f"CPT found in: {file_path}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")


# Replace the below string with your actual directory path
parent_dir = "/Hospital Price Transparency Data/OH"
search_cpt_in_json_files(parent_dir)
