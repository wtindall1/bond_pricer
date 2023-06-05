"""
Pydantic models / schemas (will be the input to db crud util functions)
"""
from pydantic import BaseModel
import uuid


class BondPricingCreate(BaseModel):
    reference: uuid.UUID
    clean_price: float
    dirty_price: float

