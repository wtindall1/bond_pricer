from sqlalchemy.orm import Session
from . import models
from . import schemas
import uuid

def get_bond_pricing(db: Session, reference: str):
    return db.query(models.BondPricing).filter(models.BondPricing.reference == reference).first()

def create_bond_pricing(db: Session, bond_pricing: schemas.BondPricingCreate):

    db_bond_pricing = models.BondPricing(
        reference = bond_pricing.reference,
        clean_price = bond_pricing.clean_price,
        dirty_price = bond_pricing.dirty_price
    )
    db.add(db_bond_pricing)
    db.commit()
    db.refresh(db_bond_pricing)
    return db_bond_pricing
