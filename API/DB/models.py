from sqlalchemy.orm import Column, Integer, Float
from .database import Base
import uuid

class BondPricing(Base):
    __tablename__ = "bond_pricings"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(uuid.UUID, unique=True, index=True)
    clean_price = Column(Float)
    dirty_price = Column(Float)
    

