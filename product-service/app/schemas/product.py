from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from typing import Optional, List
from app.models.product import ProductStatus
from datetime import datetime

class CreateProduct(BaseModel):
    name:str= Field(max_length=100, min_length=1)
    description:str 
    price:Decimal = Field(ge=0)
    quantity:int = Field(ge=0)
    category:str = Field(max_length=100, min_length=1)
    model_config = ConfigDict(str_strip_whitespace=True)

class UpdateProduct(BaseModel):
    name:Optional[str] = None        
    description:Optional[str] = None  
    price:Optional[Decimal] = None  
    quantity:Optional[int] = None  
    category:Optional[str] = None  
    status:Optional[ProductStatus] = None

class UpdateProductStatus(BaseModel):
    status:ProductStatus        

class ProductResponse(BaseModel):
    name:str
    description:str 
    price:Decimal
    quantity:int 
    category:str 
    status:ProductStatus
    createdAt:datetime
    updatedAt:datetime|None

    model_config = ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    items:List[ProductResponse]
    page:int
    size:int
    total_items:int
    total_pages:int   