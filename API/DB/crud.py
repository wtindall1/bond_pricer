from sqlalchemy.orm import Session
from . import models
from . import schemas
import uuid

def get_bond_pricing(db: Session, reference: uuid.UUID):
    return db.query(models.BondPricing).filter(models.BondPricing.reference == reference).first()

def create_bond_pricing(db: Session, bond_pricing: schemas.BondPricingCreate):
    ...