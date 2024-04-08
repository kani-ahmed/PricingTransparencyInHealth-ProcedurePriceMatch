# extract-columns-load-tables.py:

import logging
import csv
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from extensions import db
from app import app
from models.city import City
from models.zipcode import ZipCode
from models.hospital import Hospital
from models.payer import Payer

# Configure logging
logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.DEBUG, datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)


def get_or_create(session, model, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def load_data_from_csv(csv_file_path):
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            city_name = row['City']
            zip_code = row['ZipCode']
            hospital_name = row['Hospital']
            payer_name = row['payer']

            # Insert City
            city = get_or_create(db.session, City, name=city_name)

            # Insert ZipCode and link to City
            zipcode = get_or_create(db.session, ZipCode, code=zip_code, city_id=city.id)

            # Insert Hospital and link to ZipCode
            hospital = get_or_create(db.session, Hospital, name=hospital_name, zipcode_id=zipcode.id)

            # Insert Payer and ensure linkage to ZipCode
            payer = get_or_create(db.session, Payer, name=payer_name)

            # Link Payer to ZipCode if not already linked
            if zipcode not in payer.zipcodes:
                payer.zipcodes.append(zipcode)
                db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        logger.info("Starting data loading process...")
        load_data_from_csv('/data-cleaning-pipeline-generated-data/all-rows-with-only-CPT-all-csv-files-combined.csv')
        logger.info("Data loading completed successfully.")
