"""
Pydantic models / schemas (will be the input to db crud util functions)
"""
from pydantic import BaseModel
from typing import Optional
import uuid


class BondPricingCreate(BaseModel):
    reference: str
    clean_price: Optional[float]
    dirty_price: Optional[float]

