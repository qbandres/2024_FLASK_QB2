from app import db
from sqlalchemy import DateTime
from sqlalchemy import BigInteger, Integer, Text, Float, Date

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    date_created = db.Column(DateTime, nullable=False)  # Cambio de Date a DateTime
    rol = db.Column(db.String(15), nullable=False)
    proyecto = db.Column(db.String(50), nullable=True)  # Si proyecto puede ser nulo


class EstTeklaData(db.Model):
    __tablename__ = 'tekla_data'
    ID = db.Column(BigInteger, primary_key=True)
    PIECEMARK = db.Column(Text, nullable=False)
    BARCODE = db.Column(Text, nullable=False)
    ESP = db.Column(Text, nullable=False)
    PROFILE = db.Column(Text, nullable=False)
    LINEA = db.Column(Text, nullable=False)
    DESCRIPTION = db.Column(Text, nullable=False)
    CLASS = db.Column(Text, nullable=False)
    QUANTITY = db.Column(Integer, nullable=False)
    WEIGHT = db.Column(Float, nullable=False)  # double precision es Float en SQLAlchemy
    RATIO = db.Column(Float, nullable=False)  # double precision es Float en SQLAlchemy
    TRASLADO = db.Column(Date, nullable=False)
    PRE_ENSAMBLE = db.Column(Date, nullable=False)
    MONTAJE = db.Column(Date, nullable=False)
    TORQUE = db.Column(Date, nullable=False)
    PUNCH = db.Column(Date, nullable=False)