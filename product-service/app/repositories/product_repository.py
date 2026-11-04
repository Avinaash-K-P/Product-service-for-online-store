from sqlalchemy.orm import Session
from decimal import Decimal
from app.models.product import Product, ProductStatus

def get_all_products(
    db:Session,
    skip:int=0,
    limit:int=10,
    category:str=None, # type: ignore
    status:ProductStatus=None, # type: ignore        
    maxPrice:Decimal=None,# type: ignore
    minPrice:Decimal=None,# type: ignore
    sortby:str="price_asc" 
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category==category)

    if status:
        query = query.filter(Product.status==status)    

    if maxPrice:
        query = query.filter(Product.price <= maxPrice)    

    if minPrice:
        query = query.filter(Product.price >= minPrice)

    total_items = query.count()

    if sortby == "price_sort":
        query = query.order_by(Product.price.asc())

    elif sortby == "name_sort":
        query = query.order_by(Product.name.desc())        

    products =  query.offset(skip).limit(limit).all()        

    return products, total_items