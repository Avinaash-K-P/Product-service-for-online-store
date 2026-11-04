from datetime import datetime, timezone

from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.error import ErrorResponse

def create_error_response(
    status_code: int,
    error: str,
    message: str,
    path: str,
    details: list = None # type: ignore
):
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status_code,
        "error": error,
        "message": message,
        "path": path,
        "details": details or []
    }
 
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    response = create_error_response(
        status_code=exc.status_code,
        error=get_error_name(exc.status_code),
        message=str(exc.detail),
        path=request.url.path
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response,
        headers=exc.headers
    )

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    details = []

    for error in exc.errors():
        field = ".".join(str(item) for item in error["loc"] if item != "body")

        details.append({
            "field": field or "request",
            "issue": error["msg"]
        })

    response = create_error_response(
        status_code=422,
        error="Unprocessable Entity",
        message="Validation failed",
        path=request.url.path,
        details=details
    )

    return JSONResponse(
        status_code=422,
        content=response
    )

async def generic_exception_handler(
    request: Request,
    exc: Exception
):
    response = create_error_response(
        status_code=500,
        error="Internal Server Error",
        message="An unexpected error occurred",
        path=request.url.path
    )

    return JSONResponse(
        status_code=500,
        content=response
    )

def get_error_name(status_code: int) -> str:
    error_names = {
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        409: "Conflict",
        422: "Unprocessable Entity",
        500: "Internal Server Error"
    }

    return error_names.get(status_code, "HTTP Error")
