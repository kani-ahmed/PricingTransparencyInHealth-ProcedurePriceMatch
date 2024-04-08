# zipcode_payer.py

from extensions import db

zipcode_payer = db.Table('zipcode_payer',
                         db.Column('zipcode_id', db.Integer, db.ForeignKey('ZipCodes.id'), primary_key=True),
                         db.Column('payer_id', db.Integer, db.ForeignKey('Payers.id'), primary_key=True))
