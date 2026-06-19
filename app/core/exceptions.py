from fastapi import Request
from fastapi.responses import JSONResponse

class BusinessError(Exception):
    def __init__(self, code: str, message: str,
                 details: dict | None = None, status_code: int = 422):
        self.code = code
        self.message = message
        self.details = details or {}
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(BusinessError):
    def __init__(self, code: str, message: str, details: dict | None = None):
        super().__init__(code, message, details, status_code=404)

async def business_error_handler(request: Request, exc: BusinessError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.code,
            "message": exc.message,
            "details": exc.details,
        },
    )
