# load data-data-mysql.py in the root folder:

import logging
from extensions import db
from app import app
from models.hospital_charge import HospitalCharge
from models.cpt_translation import CptTranslation
import csv

# Configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def load_csv_data(csv_file_path, model, is_cpt_translation=False):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        entries = []
        for row in reader:
            if is_cpt_translation:
                # For the CptTranslations table
                cpt_code = row['CPT Code']
                if not CptTranslation.query.get(cpt_code):
                    db_entry = model(CPT_Code=cpt_code, Description=row['Description'])
                    entries.append(db_entry)
            else:
                # For the HospitalCharges table
                associated_codes = row['Associated_Codes']
                if CptTranslation.query.get(associated_codes):
                    cash_discount = row['Cash_Discount']
                    if cash_discount == 'N/A':
                        cash_discount = None  # Set 'N/A' to None for Numeric columns

                    deidentified_min_allowed = row['Deidentified_Min_Allowed']
                    if deidentified_min_allowed == 'N/A':
                        deidentified_min_allowed = None  # Set 'N/A' to None for Numeric columns

                    db_entry = model(
                        Associated_Codes=associated_codes,
                        Cash_Discount=cash_discount,
                        Deidentified_Max_Allowed=row.get('Deidentified_Max_Allowed', 'N/A'),
                        Deidentified_Min_Allowed=deidentified_min_allowed,
                        payer=row['payer'],
                        iobSelection=row['iobSelection'],
                        City=row['City'],
                        ZipCode=row['ZipCode'],
                        Hospital=row['Hospital']
                    )
                    entries.append(db_entry)
                else:
                    logger.warning(f"Skipping row with Associated_Codes '{associated_codes}' as it does not exist in CptTranslations")

        logger.debug(f"Loaded {len(entries)} entries from {csv_file_path}")
        db.session.add_all(entries)
        db.session.commit()
        logger.info(f"Successfully committed {len(entries)} entries to the database")


# Example usage
if __name__ == "__main__":
    with app.app_context():
        # Load CptTranslations data first
        logger.info("Loading CptTranslations data...")
        load_csv_data('/cpt-translation.csv',
                      CptTranslation, True)
        logger.info("CptTranslations data loaded successfully")

        # Load HospitalCharges data after CptTranslations
        logger.info("Loading HospitalCharges data...")
        load_csv_data('/data-cleaning-pipeline-generated-data/all-rows-with-only-CPT-all-csv-files-combined.csv',
                      HospitalCharge)
        logger.info("HospitalCharges data loaded successfully")