from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


SQLALCHEMY_DATABASE_URL = "sqlite:///./local_dev.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

#class to create sessions later on
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#db models will inherit from this
Base = declarative_base()
