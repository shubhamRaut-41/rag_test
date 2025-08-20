from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

class CustomError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

def handle_custom_error(exc: CustomError):
    return HTTPException(status_code=exc.status_code, detail=exc.message)

def handle_not_found_error(detail: str = "Resource not found."):
    return HTTPException(status_code=HTTP_404_NOT_FOUND, detail=detail)

def handle_bad_request_error(detail: str = "Bad request."):
    return HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=detail)

def handle_internal_server_error(detail: str = "Internal server error."):
    return HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)