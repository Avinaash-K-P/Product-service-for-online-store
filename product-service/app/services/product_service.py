from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.product import Product, ProductStatus
from app.schemas.product import CreateProduct, UpdateProduct, UpdateProductStatus
from datetime import datetime
from decimal import Decimal
from app.repositories.product_repository import get_all_products
import math
from datetime import datetime

def create_product(db:Session, payload:CreateProduct):

    name_exist = db.query(Product).filter(
        Product.name == payload.name
    ).first()

    if name_exist:
        raise HTTPException(status_code=409, detail="product name already exist")

    product = Product(
        name = payload.name,
        description = payload.description,
        price = payload.price,
        quantity = payload.quantity,
        category = payload.category,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

def get_product_list(
        db:Session, 
        skip:int=0, 
        limit:int=10,
        category:str=None,# type: ignore
        status:ProductStatus=None,# type: ignore
        maxPrice:Decimal=None,# type: ignore
        minPrice:Decimal=None,# type: ignore
        sortby:str="price_asc"
    ):

    products, total_items =  get_all_products(
        db=db,
        skip=skip,
        limit=limit,
        category=category,
        status=status,
        maxPrice=maxPrice,
        minPrice=minPrice,
        sortby=sortby
    )

    total_pages = math.ceil(total_items/limit)

    return {
        "items": products,
        "page": (skip//limit)+1,
        "size": limit,
        "total_items": total_items,
        "total_pages": total_pages 
    }

def get_product_by_id(db:Session, product_id:int):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product

def updated_product(db:Session, payload:UpdateProduct, product_id:int):

    product = get_product_by_id(db,product_id)

    product.name = payload.name #type:ignore
    product.description = payload.description #type:ignore
    product.price = payload.price #type:ignore
    product.quantity = payload.quantity #type:ignore
    product.category = payload.category #type:ignore
    product.status = payload.status #type:ignore
    product.updatedAt = datetime.utcnow() #type:ignore

    db.commit()
    db.refresh(product)

    return product

def update_product_status(db:Session, payload:UpdateProductStatus, product_id:int):

    product = get_product_by_id(db, product_id)

    product.status = payload.status #type:ignore

    db.commit()
    db.refresh(product)

    message = ""

    if product.status == ProductStatus.ACTIVE: # type: ignore
        message = "Product is enabled"
    else:
        message = "Product is disabled"

    return {
        "message": message
    }    

def delete_product(db:Session, product_id:int):

    product = get_product_by_id(db, product_id)

    db.delete(product)
    db.commit()

