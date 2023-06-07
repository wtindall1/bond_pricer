import pytest
import sys
sys.path.append("..")
from API.DB import models, schemas, crud
from API.DB.database import SessionLocal, Base, engine


@pytest.fixture(scope="module")
def db_connection():
    db = SessionLocal()
    yield db
    #undo changes so test records don't persist
    db.rollback()
    db.close()

@pytest.fixture(scope="module")
def valid_bond_pricing():
    valid_bond_pricing = schemas.BondPricingCreate(reference="ccb2cdc6-a648-4117-85b5-2d983266dca9", clean_price=100, dirty_price=101)
    return valid_bond_pricing

class TestDBUtils:

    def test_create_bond_pricing(self, db_connection, valid_bond_pricing):

        #saves record in db and returns sqlalchemy model object
        db_bond_pricing = crud.create_bond_pricing(db=db_connection, bond_pricing=valid_bond_pricing)

        #query db for record with same reference
        retrieved_bond_pricing = crud.get_bond_pricing(db=db_connection, reference= db_bond_pricing.reference)

        assert db_bond_pricing == retrieved_bond_pricing













