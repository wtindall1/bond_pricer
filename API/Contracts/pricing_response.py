from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class BondPricingResponse(BaseModel):
    reference: str
    clean_price: Optional[float]
    dirty_price: Optional[float]

