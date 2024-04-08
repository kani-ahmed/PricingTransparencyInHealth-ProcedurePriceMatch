# models/icd_cpt_mapping.py
from extensions import db


class IcdCptMapping(db.Model):
    __tablename__ = 'IcdCptMappings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ICD_Code = db.Column(db.String(255), nullable=False)
    CPT_Code = db.Column(db.String(255), db.ForeignKey('CptTranslations.CPT_Code'), nullable=False)

    # Relationship with the CptTranslation model
    cpt_translation = db.relationship('CptTranslation', backref=db.backref('icd_cpt_mappings', lazy='dynamic'))
