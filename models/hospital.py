# models/hospital.py
from extensions import db


class Hospital(db.Model):
    __tablename__ = 'Hospitals'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    zipcode_id = db.Column(db.Integer, db.ForeignKey('ZipCodes.id'), nullable=False)
