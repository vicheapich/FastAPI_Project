from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATAASE_URL = 'postgresql://vichea:1234@localhost/fastapi_db'

engine = create_engine(SQLALCHEMY_DATAASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autocommit = False ,autoflush=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()