# extract-searchable-fields.py

import csv
import os

# Set the path to the input file
input_file = '/data-cleaning-pipeline-generated-data/all-rows-with-only-CPT-all-csv-files-combined.csv'

# Set the output directory
output_dir = '//'

# Initialize sets to store unique values
cities = set()
zipcodes = set()
hospitals = set()
payers = set()

# Read the input file and extract the values
with open(input_file, 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        cities.add(row['City'])
        zipcodes.add(row['ZipCode'])
        hospitals.add(row['Hospital'])
        payers.add(row['payer'])

# Save unique cities to a file
with open(os.path.join(output_dir, 'data-cleaning-pipeline-generated-data-city.csv'), 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['City'])
    csv_writer.writerows([[city] for city in cities])

# Save unique zipcodes to a file
with open(os.path.join(output_dir, 'data-cleaning-pipeline-generated-data-zipcode.csv'), 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['ZipCode'])
    csv_writer.writerows([[zipcode] for zipcode in zipcodes])

# Save unique hospitals to a file
with open(os.path.join(output_dir, 'data-cleaning-pipeline-generated-data-hospital.csv'), 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Hospital'])
    csv_writer.writerows([[hospital] for hospital in hospitals])

# Save unique payers to a file
with open(os.path.join(output_dir, 'data-cleaning-pipeline-generated-data-payer.csv'), 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(['Payer'])
    csv_writer.writerows([[payer] for payer in payers])

# Output the count of unique values saved
print(f"Saved {len(cities)} unique cities to data-cleaning-pipeline-generated-data-city.csv")
print(f"Saved {len(zipcodes)} unique zipcodes to data-cleaning-pipeline-generated-data-zipcode.csv")
print(f"Saved {len(hospitals)} unique hospitals to data-cleaning-pipeline-generated-data-hospital.csv")
print(f"Saved {len(payers)} unique payers to data-cleaning-pipeline-generated-data-payer.csv")