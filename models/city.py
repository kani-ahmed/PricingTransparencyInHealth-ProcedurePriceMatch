# models/city.py
from extensions import db


class City(db.Model):
    __tablename__ = 'Cities'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    zipcodes = db.relationship('ZipCode', backref='city', lazy=True)
