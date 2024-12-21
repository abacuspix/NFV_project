from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# SQLite database URI
DATABASE_URI = 'sqlite:///my_catalog.db'

# SQLAlchemy engine
engine = create_engine(DATABASE_URI, echo=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

# Base class for models
class Base(DeclarativeBase):
    pass
