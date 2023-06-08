from fastapi import FastAPI
from pydantic import BaseModel, Field, validator
from datetime import date
from typing import Optional
import sys
sys.path.append("..")
from Application.CreditRating import CreditRating

class BondPricingRequest(BaseModel):
    face_value: float = Field(..., ge=0)
    interest_rate: float = Field(..., ge=0)
    coupon_frequency: int = Field(..., ge=0, le=12)
    maturity_date: date = Field(..., description="Date in format YYYY-MM-DD")
    credit_rating: CreditRating 

    @validator("maturity_date", "credit_rating")
    def validate_fields(cls, value, field):
        if field.name == "maturity_date":
            if value <= date.today():
                raise ValueError("maturity_date must be a future date")
            elif value > date(2200,1,1):
                raise ValueError("maturity_date must be before 2200-01-01")
            return value
        
        if field.name == "credit_rating":
            if value not in CreditRating:
                raise ValueError("credit_rating must be a valid S&P / Fitch rating")
            return value



    class Config:
        schema_extra = {
            "example": {
                "face_value": 100,
                "interest_rate": 0.1,
                "coupon_frequency": 2,
                "maturity_date": "2030-11-30",
                "credit_rating": "AAA"
            }
        }



