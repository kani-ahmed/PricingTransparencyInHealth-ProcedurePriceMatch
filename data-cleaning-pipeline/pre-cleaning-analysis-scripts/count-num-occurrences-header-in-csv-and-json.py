import os
import json
import pandas as pd


def search_associated_codes_in_files(parent_dir):
    json_count = 0
    csv_count = 0
    json_associated_codes_count = 0
    csv_associated_codes_count = 0

    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith('.json'):
                json_count += 1
                try:
                    with open(file_path, 'r', encoding='utf-8-sig') as f:
                        data = json.load(f)
                        data_str = json.dumps(data)
                        if "iobSelection" in data_str:
                            json_associated_codes_count += 1
                except Exception as e:
                    print(f"Skipping file {file_path} due to error: {e}")
            elif file.endswith('.csv'):
                csv_count += 1
                try:
                    df = pd.read_csv(file_path, nrows=1, encoding='latin-1')
                    if 'Associated_Codes' in df.columns:
                        csv_associated_codes_count += 1
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    print(f"Total number of JSON files: {json_count}")
    print(f"Total number of CSV files: {csv_count}")
    print(f"Total JSON files containing 'Associated_Codes': {json_associated_codes_count}")
    print(f"Total CSV files containing 'Associated_Codes': {csv_associated_codes_count}")


# Replace the below string with your actual directory path
parent_dir = "/Hospital Price Transparency Data/OH"
search_associated_codes_in_files(parent_dir)
