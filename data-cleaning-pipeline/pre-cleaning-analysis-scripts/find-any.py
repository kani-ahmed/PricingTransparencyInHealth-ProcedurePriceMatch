import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor


def search_iob_selection_in_csv_file(file_path):
    try:
        for chunk in pd.read_csv(file_path, chunksize=600, low_memory=False):
            if 'iobSelection' in chunk.to_string():
                print(f"iobSelection found in: {file_path}")
                return 1
    except Exception as e:
        pass
    return 0


def search_iob_selection_in_csv_files(parent_dir):
    csv_files = []
    for root, dirs, files in os.walk(parent_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                csv_files.append(file_path)

    csv_count = len(csv_files)

    with ProcessPoolExecutor() as executor:
        csv_iob_selection_count = sum(executor.map(search_iob_selection_in_csv_file, csv_files))

    print(f"Total number of CSV files: {csv_count}")
    print(f"Total CSV files containing 'iobSelection': {csv_iob_selection_count}")


if __name__ == '__main__':
    # Replace the below string with your actual directory path
    parent_dir = "/Hospital Price Transparency Data/OH"
    search_iob_selection_in_csv_files(parent_dir)
