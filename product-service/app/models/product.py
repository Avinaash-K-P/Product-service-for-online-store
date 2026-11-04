from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, Numeric, Enum as SQLEnum, DateTime
from enum import Enum 
from datetime import datetime

class ProductStatus(str, Enum):
    ACTIVE="active" 
    INACTIVE="inactive"

class Product(Base):

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    description = Column(Text, nullable=False)

    price = Column(Numeric(10,2), nullable=False)

    quantity = Column(Integer, nullable=False)

    category = Column(String(100), nullable=False)

    status = Column(SQLEnum(ProductStatus), default=ProductStatus.ACTIVE, nullable=False)

    createdAt = Column(DateTime, default=datetime.utcnow, nullable=False)

    updatedAt = Column(DateTime, nullable=True)     
