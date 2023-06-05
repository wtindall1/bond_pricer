from fastapi import FastAPI
from Contracts.pricing_request import BondPricingRequest
from Contracts.pricing_response import BondPricingResponse
from Application.Bond import Bond
from Application.ValuationPV import ValuationPV
from Application.CreditRating import CreditRating
import uuid

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/bond_price")
async def price(request: BondPricingRequest):
    
    bond = Bond(
        face_value=request.face_value,
        interest_rate=request.interest_rate,
        coupon_frequency=request.coupon_frequency,
        maturity_date=request.maturity_date,
        credit_rating=request.credit_rating
    )

    valuation = ValuationPV(bond)
    price = valuation.price(discount_rate_specified=request.discount_rate)

    response = BondPricingResponse(
        reference = uuid.uuid4(),
        clean_price=price["CleanPrice"],
        dirty_price=price["DirtyPrice"]
    )
    
    return response