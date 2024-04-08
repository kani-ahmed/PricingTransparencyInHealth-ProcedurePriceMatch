# cpt_translation.py in models/cpt_translation.py

from extensions import db


class CptTranslation(db.Model):
    __tablename__ = 'CptTranslations'

    CPT_Code = db.Column(db.String(255), primary_key=True)
    Description = db.Column(db.Text)
