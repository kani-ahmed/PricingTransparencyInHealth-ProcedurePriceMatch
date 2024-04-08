# load_icd_cpt_mappings.py in the root folder:

import os
import csv
import logging
from app import app
from models.icd_cpt_mapping import IcdCptMapping
from models.cpt_translation import CptTranslation
from extensions import db

# Configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def load_icd_cpt_mappings(code_mappings_directory):
    # Get all CPT codes from the CptTranslation table and store in a set for quick lookup
    existing_cpt_codes = {cpt.CPT_Code for cpt in CptTranslation.query.all()}

    files = os.listdir(code_mappings_directory)
    for file in files:
        if file.endswith('_code_mappings.csv'):
            cpt_code = file.split('_')[0]
            if cpt_code not in existing_cpt_codes:
                logger.warning(
                    f"CPT code {cpt_code} from file {file} does not exist in CptTranslations table. Skipping file.")
                continue
            csv_file_path = os.path.join(code_mappings_directory, file)
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    icd_code = row['Diagnosis Code']
                    icd_cpt_mapping = IcdCptMapping(ICD_Code=icd_code, CPT_Code=cpt_code)
                    db.session.add(icd_cpt_mapping)
                try:
                    db.session.commit()
                    logger.info(f"Successfully committed ICD-CPT mappings from {file}")
                except Exception as e:
                    db.session.rollback()
                    logger.error(f"An error occurred while inserting data from {file}: {e}")


# Example usage
if __name__ == "__main__":
    code_mappings_directory = '/Users/kani/PycharmProjects/Hospital_Price_Transparency_Project/COLLECTED-CPT-ICD10-CM-CODE_MAPPINGS'
    with app.app_context():
        logger.info("Loading ICD-CPT mappings data...")
        load_icd_cpt_mappings(code_mappings_directory)
        logger.info("ICD-CPT mappings data loaded successfully")
