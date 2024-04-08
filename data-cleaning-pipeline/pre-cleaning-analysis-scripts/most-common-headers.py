import os
import pandas as pd
from collections import Counter


def extract_common_column_names(parent_dir):
    column_names = []

    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    df = pd.read_csv(file_path, nrows=0)
                    column_names.extend(df.columns)
                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

    column_name_counts = Counter(column_names)
    sorted_column_names = sorted(column_name_counts.items(), key=lambda x: x[1], reverse=True)

    print("Most common column names:")
    for column_name, count in sorted_column_names:
        print(f"{column_name}: {count}")


# Replace the below string with your actual directory path
parent_dir = "/Hospital Price Transparency Data/OH"
extract_common_column_names(parent_dir)
