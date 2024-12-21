from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from my_app.database import Base

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)

    # Relationship with products
    products = relationship("Product", back_populates="category")


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    key = Column(String(100), nullable=False, unique=True)  # Ensure 'key' is defined here
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=True)

    category = relationship("Category", back_populates="products")


