from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
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

#rate limiting
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

#add limiter to app and handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


#db dependency to provide session
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/")
async def root():
    return {"message": "Add ""/docs"" to the url to try the bond pricer"}



@app.get("/bond_price/{reference}", response_model=BondPricingResponse)
@limiter.limit("20/minute")
async def get_price(request: Request, reference: str, db: Session = Depends(get_db_session)) -> BondPricingResponse:
    
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
@limiter.limit("20/minute")
async def create_price(request: Request, bond_request: BondPricingRequest, db: Session = Depends(get_db_session)) -> BondPricingResponse:
    
    #create bond object
    bond = Bond(
        face_value=bond_request.face_value,
        interest_rate=bond_request.interest_rate,
        coupon_frequency=bond_request.coupon_frequency,
        maturity_date=bond_request.maturity_date,
        credit_rating=bond_request.credit_rating
    )


    #valuation
    valuation = ValuationPV(bond)
    price = valuation.price_with_simulated_yields()
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