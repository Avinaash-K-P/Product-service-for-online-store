import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException

from app.services.product_service import (
    create_product,
    get_product_by_id
)
from app.models.product import Product
from app.schemas.product import CreateProduct
from decimal import Decimal

def test_create_product_success():
    
    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    payload = CreateProduct(
        name="Laptop",
        description="Test laptop",
        price=Decimal("50000"),
        quantity=10,
        category="Electronics"
    )

    result = create_product(db, payload)

    assert isinstance(result, Product)
    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once()


def test_create_product_duplicate_name():
    
    db = MagicMock()

    existing_product = Product(name="Laptop")

    db.query.return_value.filter.return_value.first.return_value = existing_product

    payload = CreateProduct(
        name="Laptop",
        description="Test laptop",
        price=Decimal("50000"),
        quantity=10,
        category="Electronics"
    )

    with pytest.raises(HTTPException) as exc_info:
        create_product(db, payload)

    assert exc_info.value.status_code == 409
    db.add.assert_not_called()


def test_get_product_by_id_success():

    db = MagicMock()

    existing_product = Product(id=1, name="Laptop")

    db.query.return_value.filter.return_value.first.return_value = existing_product

    result = get_product_by_id(db, 1)

    assert result == existing_product
    assert result.id == 1 #type:ignore


def test_get_product_by_id_not_found():

    db = MagicMock()

    db.query.return_value.filter.return_value.first.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        get_product_by_id(db, 999)

    assert exc_info.value.status_code == 404
