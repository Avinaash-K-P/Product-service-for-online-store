from fastapi import FastAPI
from app.routes.product import router as product_router
from app.core.exceptions import (
    http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title="Product Service for Online Store")

app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler # type: ignore
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler # type: ignore
)

app.add_exception_handler(
    Exception,
    generic_exception_handler
)

app.include_router(product_router)

@app.get("/")
def read_root():
    return{
        "message":"Product Service working"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }