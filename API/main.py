from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from Contracts.pricing_request import BondPricingRequest
from Contracts.pricing_response import BondPricingResponse
from Application.Bond import Bond
from Application.ValuationPV import ValuationPV
from Application.CreditRating import CreditRating
from DB import models, schemas, crud
from DB.database import engine, SessionLocal
import uuid

#create the db tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


#db dependency to provide session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
    return {"message": "Hello World"}



@app.get("/bond_price/{reference}", response_model=BondPricingResponse)
async def get_price(reference: str, db: Session = Depends(get_db_session)) -> BondPricingResponse:
    
    #query table for pricing
    db_bond_pricing = crud.get_bond_pricing(db, reference)
    if db_bond_pricing is None:
        #404 if no record with matching reference
        raise HTTPException(status_code=404, detail="Pricing record not found")
     
    #return response object
    response = BondPricingResponse(
        reference=db_bond_pricing.reference,
        clean_price=db_bond_pricing.clean_price,
        dirty_price=db_bond_pricing.dirty_price
    )
    return response
    

@app.post("/bond_price", response_model=BondPricingResponse)
async def create_price(request: BondPricingRequest, db: Session = Depends(get_db_session)) -> BondPricingResponse:
    
    #create bond object
    bond = Bond(
        face_value=request.face_value,
        interest_rate=request.interest_rate,
        coupon_frequency=request.coupon_frequency,
        maturity_date=request.maturity_date,
        credit_rating=request.credit_rating
    )


    #valuation
    valuation = ValuationPV(bond)
    price = valuation.price(discount_rate_specified=request.discount_rate)
    reference = str(uuid.uuid4())


    #create db record
    db_bond_pricing = schemas.BondPricingCreate(
        reference=reference,
        clean_price=price["CleanPrice"],
        dirty_price=price["DirtyPrice"]
    )
    #save to db
    crud.create_bond_pricing(db=db, bond_pricing=db_bond_pricing)


    #create response object and return it
    response = BondPricingResponse(
        reference = reference,
        clean_price=price["CleanPrice"],
        dirty_price=price["DirtyPrice"]
    )
    return response