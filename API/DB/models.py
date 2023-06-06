"""
SQLAlchemy models which will be the output to crud.py functions
"""
from sqlalchemy import Column, Integer, Float, String
from .database import Base
import uuid

class BondPricing(Base):
    __tablename__ = "bond_pricings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    reference = Column(String(36), unique=True, index=True)
    clean_price = Column(Float)
    dirty_price = Column(Float)


