from fastapi import APIRouter, Depends, Query
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.schemas.product import (
    CreateProduct,
    UpdateProduct,
    UpdateProductStatus,
    ProductResponse,
    ProductListResponse,
    ProductStatus
)
from app.services.product_service import (
    create_product,
    get_product_by_id,
    get_product_list,
    updated_product,
    update_product_status,
    delete_product
)
from typing import Optional
from decimal import Decimal
from app.core.config import settings

router = APIRouter(prefix=settings.API_PREFIX, tags=["Product Management"])

@router.post("/", response_model=ProductResponse)
def add_product(
    payload: CreateProduct,
    db:Session=Depends(get_db)
):
    return create_product(db=db, payload=payload)

@router.get("/", response_model=ProductListResponse)
def list_products(
    skip:int=Query(default=0, ge=0),
    limit:int=Query(default=10, ge=1, le=100),
    category:Optional[str]=Query(default=None),
    status:Optional[ProductStatus]=Query(default=None),
    maxPrice:Optional[Decimal]=Query(default=None, ge=0),
    minPrice:Optional[Decimal]=Query(default=None, ge=0),
    sort_by:str = Query(default="price_asc"),
    db:Session=Depends(get_db)
):
    return get_product_list(
        db=db, 
        skip=skip, 
        limit=limit,
        category=category, # type: ignore
        status=status, # type: ignore
        maxPrice=maxPrice, # type: ignore
        minPrice=minPrice, # type: ignore
        sortby=sort_by
        )

@router.get("/{id}", response_model=ProductResponse)
def view_product(
    id:int,
    db:Session=Depends(get_db)
):
    return get_product_by_id(db=db, product_id=id)

@router.put("/{id}", response_model=ProductResponse)
def edit_product(
    id:int,
    payload: UpdateProduct,
    db:Session=Depends(get_db)
):
    return updated_product(db=db, payload=payload, product_id=id)

@router.patch("/{id}")
def edit_product_status(
    id:int,
    payload: UpdateProductStatus,
    db:Session=Depends(get_db)
):
    return update_product_status(db=db, payload=payload, product_id=id)

@router.delete("/{id}", status_code=204)
def remove_product(
    id:int,
    db:Session=Depends(get_db)
):
    return delete_product(db=db, product_id=id)