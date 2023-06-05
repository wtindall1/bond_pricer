from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import date
import uuid


class BondPricingResponse(BaseModel):
    reference: uuid.UUID
    clean_price: float
    dirty_price: float

