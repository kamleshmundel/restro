from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError
from app.middleware.response_middleware import build_response

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errs = []
    for e in exc.errors():
        field = e.get("loc")[-1]
        print(e["type"])
        msg = f"{field.capitalize()} is required" if e["type"] == "missing" else e["msg"]
        errs.append(msg)
    return JSONResponse(build_response(None, 422, ", ".join(errs)), status_code=422)
