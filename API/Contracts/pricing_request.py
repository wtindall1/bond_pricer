from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import date
from typing import Optional

class BondPricingRequest(BaseModel):
    face_value: float = Field(..., ge=0)
    interest_rate: float = Field(..., ge=0)
    coupon_frequency: int = Field(..., ge=0)
    maturity_date: date = Field(..., description="Date in format YYYY-MM-DD")
    credit_rating: str 
    discount_rate: Optional[float] = None
