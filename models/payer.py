# models/payer.py
from extensions import db


class Payer(db.Model):
    __tablename__ = 'Payers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    zipcodes = db.relationship('ZipCode', secondary='zipcode_payer', lazy='subquery',
                               backref=db.backref('payers', lazy=True))

