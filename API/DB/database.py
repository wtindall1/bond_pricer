from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

password = os.environ.get("db_password")
SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{password}@localhost:5432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#class to create sessions later on
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#db models will inherit from this
Base = declarative_base()
