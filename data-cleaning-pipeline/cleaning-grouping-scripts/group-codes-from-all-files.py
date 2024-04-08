import os
import csv


def process_csv_files(directory):
    print("Processing CSV files...")
    # Create the folders for each code type in the current directory
    current_dir = os.getcwd()
    os.makedirs(os.path.join(current_dir, "CPT_CODES"), exist_ok=True)
    os.makedirs(os.path.join(current_dir, "HCPCS_CODES"), exist_ok=True)
    os.makedirs(os.path.join(current_dir, "ICD-10-PCS_CODES"), exist_ok=True)

    cpt_codes = set()
    hcpcs_codes = set()
    icd_10_pcs_codes = set()

    # Iterate through each file and subdirectory in the directory
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".csv"):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")

                # Open the .csv file and read the rows
                with open(file_path, "r") as file:
                    csv_reader = csv.reader(file)
                    next(csv_reader)  # Skip the header row

                    for row in csv_reader:
                        if len(row) > 0:
                            code = row[0].strip()

                            # Determine the code type and add it to the respective set
                            if code.isdigit() and len(code) == 5:
                                cpt_codes.add(code)
                                print(f"CPT code found: {code}")
                            elif code.isalnum() and len(code) == 5 and code[0].isalpha():
                                hcpcs_codes.add(code)
                                print(f"HCPCS code found: {code}")
                            elif (code.isdigit() and len(code) == 3) or (code.isalnum() and len(code) == 7):
                                icd_10_pcs_codes.add(code)
                                print(f"ICD-10-PCS code found: {code}")

    # Write the codes to separate files in the current directory
    cpt_codes_file = os.path.join(current_dir, "CPT_CODES", "cpt_codes.txt")
    with open(cpt_codes_file, "w") as file:
        file.write("\n".join(cpt_codes))
    print(f"CPT codes saved to: {cpt_codes_file}")

    hcpcs_codes_file = os.path.join(current_dir, "HCPCS_CODES", "hcpcs_codes.txt")
    with open(hcpcs_codes_file, "w") as file:
        file.write("\n".join(hcpcs_codes))
    print(f"HCPCS codes saved to: {hcpcs_codes_file}")

    icd_10_pcs_codes_file = os.path.join(current_dir, "ICD-10-PCS_CODES", "icd_10_pcs_codes.txt")
    with open(icd_10_pcs_codes_file, "w") as file:
        file.write("\n".join(icd_10_pcs_codes))
    print(f"ICD-10-PCS codes saved to: {icd_10_pcs_codes_file}")

    print("Processing complete.")
    print(f"Total CPT codes found: {len(cpt_codes)}")
    print(f"Total HCPCS codes found: {len(hcpcs_codes)}")
    print(f"Total ICD-10-PCS codes found: {len(icd_10_pcs_codes)}")


def main():
    # Set the path to the root directory containing the .csv files
    root_directory = "/Users/kani/PycharmProjects/Hospital_Price_Transparency_Project/all-csv-files-with-common-headers"

    # Process the .csv files in the root directory and its subdirectories
    process_csv_files(root_directory)


if __name__ == "__main__":
    main()
