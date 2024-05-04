import os
import re


def count_detailed_file_types_and_locations(parent_dir):
    json_count = 0
    csv_count = 0
    xlsx_count = 0
    hospitals_count = 0
    txt_count = 0
    json_cities = set()
    csv_cities = set()
    xlsx_cities = set()
    json_zip_codes = set()
    csv_zip_codes = set()
    xlsx_zip_codes = set()
    cities_no_csv_or_json = set()
    hospitals_with_files = set()
    all_cities = set()

    # Regex to match hospital names (all caps and underscores, optional hyphen)
    hospital_name_pattern = re.compile(r'^[A-Z_\-]+$')
    # Regex to match 5 digit zip codes
    zip_code_pattern = re.compile(r'^\d{5}$')

    for root, dirs, files in os.walk(parent_dir):
        # Extract city, zipcode, and hospital from the directory path
        parts = root.split(os.sep)
        if len(parts) >= 3 and zip_code_pattern.match(parts[-2]) and hospital_name_pattern.match(parts[-1]):
            city, zipcode, hospital = parts[-3], parts[-2], parts[-1]
            full_hospital_identifier = (city, zipcode, hospital)  # Tuple to identify the hospital

            # Count the number of files by type and check for the presence of any relevant files
            found_relevant_files = False
            for filename in files:
                if filename.endswith(".csv"):
                    csv_count += 1
                    csv_cities.add(city)
                    csv_zip_codes.add(zipcode)
                    all_cities.add(city)
                    if full_hospital_identifier not in hospitals_with_files:
                        hospitals_with_files.add(full_hospital_identifier)
                elif filename.endswith(".json"):
                    json_count += 1
                    json_cities.add(city)
                    json_zip_codes.add(zipcode)
                    all_cities.add(city)
                    if full_hospital_identifier not in hospitals_with_files:
                        hospitals_with_files.add(full_hospital_identifier)
                elif filename.endswith(".xlsx"):
                    xlsx_count += 1
                    xlsx_cities.add(city)
                    xlsx_zip_codes.add(zipcode)
                    all_cities.add(city)
                    if full_hospital_identifier not in hospitals_with_files:
                        hospitals_with_files.add(full_hospital_identifier)
                else:
                    # print file type if not recognized
                    txt_count += 1
                    # This hospital directory has no relevant files
                    all_cities.add(city)
                    if full_hospital_identifier not in hospitals_with_files:
                        hospitals_with_files.add(full_hospital_identifier)
                    # cities_no_csv_or_json.add(city)

    # Compute the count of hospitals that have relevant files
    hospitals_count = len(hospitals_with_files)
    print(f"txt files: {txt_count}")

    # Diagnostic information
    exclusive_csv_cities = csv_cities - json_cities - xlsx_cities
    exclusive_json_cities = json_cities - csv_cities - xlsx_cities
    exclusive_xlsx_cities = xlsx_cities - csv_cities - json_cities

    # Print summary
    print_summary(json_count, csv_count, xlsx_count, all_cities, csv_cities, json_cities, xlsx_cities,
                  exclusive_csv_cities, exclusive_json_cities, exclusive_xlsx_cities, cities_no_csv_or_json,
                  hospitals_count)

    print(f"xlsx_cities: {xlsx_cities}")


def print_summary(json_count, csv_count, xlsx_count, all_cities, csv_cities, json_cities, xlsx_cities,
                  exclusive_csv_cities, exclusive_json_cities, exclusive_xlsx_cities, cities_no_csv_or_json,
                  hospitals_count):
    print(f"Total number of JSON files: {json_count}")
    print(f"Total number of CSV files: {csv_count}")
    print(f"Total number of XLSX files: {xlsx_count}")
    print(f"Total number of cities data collected from: {len(all_cities)}")
    print(f"Total number of cities with CSV: {len(csv_cities)}")
    print(f"Total number of cities with JSON: {len(json_cities)}")
    print(f"Total number of cities with XLSX: {len(xlsx_cities)}")
    print(f"Total cities with exclusive CSV: {len(exclusive_csv_cities)}")
    print(f"Total cities with exclusive JSON: {len(exclusive_json_cities)}")
    print(f"Total cities with exclusive XLSX: {len(exclusive_xlsx_cities)}")
    print(f"Total cities with no CSV or JSON: {len(cities_no_csv_or_json)}")
    print(f"Total hospitals with files: {hospitals_count}")


parent_dir = "/Users/kani/PycharmProjects/Hospital_Price_Transparency_Project/Hospital Price Transparency Data/OH"
count_detailed_file_types_and_locations(parent_dir)
