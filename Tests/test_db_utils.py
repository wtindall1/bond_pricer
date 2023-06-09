import pytest
import sys
sys.path.append("..")
from API.DB import models, schemas, crud
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

#connect to test db
password = os.environ.get("db_password")
TEST_DB_URL = f"postgresql://postgres:{password}@localhost:5432/test_bond_pricing"
engine = create_engine(TEST_DB_URL)
TestSessionLocal = sessionmaker(bind=engine)

#create the db tables
models.Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def db_connection():
    db = TestSessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="module")
def valid_bond_pricing():
    valid_bond_pricing = schemas.BondPricingCreate(reference=str(uuid.uuid4()), clean_price=100, dirty_price=101)
    return valid_bond_pricing

class TestDBUtils:

    def test_create_bond_pricing(self, db_connection, valid_bond_pricing):

        #saves record in db and returns sqlalchemy model object
        db_bond_pricing = crud.create_bond_pricing(db=db_connection, bond_pricing=valid_bond_pricing)

        #query db for record with same reference
        retrieved_bond_pricing = crud.get_bond_pricing(db=db_connection, reference= db_bond_pricing.reference)

        assert db_bond_pricing == retrieved_bond_pricing













