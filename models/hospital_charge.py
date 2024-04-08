# hospital_charge model in models/hospital_charge.py

from extensions import db
from models.cpt_translation import CptTranslation


class HospitalCharge(db.Model):
    __tablename__ = 'HospitalCharges'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Associated_Codes = db.Column(db.String(255), db.ForeignKey('CptTranslations.CPT_Code'), nullable=False)
    Cash_Discount = db.Column(db.Numeric(10, 2), nullable=True)
    Deidentified_Max_Allowed = db.Column(db.String(255), nullable=True)
    Deidentified_Min_Allowed = db.Column(db.Numeric(10, 2), nullable=True)
    payer = db.Column(db.String(255), nullable=True)
    iobSelection = db.Column(db.String(255), nullable=True)
    City = db.Column(db.String(255), nullable=False)
    ZipCode = db.Column(db.String(255), nullable=False)
    Hospital = db.Column(db.String(255), nullable=False)

    cpt_translation = db.relationship('CptTranslation', backref='hospital_charges')