from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_URI

engine = create_engine(DB_URI, echo=True)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
