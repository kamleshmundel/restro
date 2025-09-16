from fastapi import FastAPI, Request, HTTPException
from app.controllers import router as app_routers

from fastapi.middleware.cors import CORSMiddleware
from app.middleware.response_middleware import WrapResponseMiddleware
from app.middleware.exception_handler import validation_exception_handler
from fastapi.exception_handlers import RequestValidationError

allowed_origins = ['*']

app = FastAPI(
    title="Restro App",
    description="A well-structured FastAPI application",
    version="1.0.0",
    root_path='/api'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # put your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request, call_next):
    print("Incoming:", request.method, request.url)
    response = await call_next(request)
    print("Response headers:", dict(response.headers))
    return response

@app.middleware("http")
async def block_unallowed_origins(request: Request, call_next):
    origin = request.headers.get("origin")
    if allowed_origins != ["*"] and origin and origin not in allowed_origins:
        raise HTTPException(status_code=403, detail="Origin not allowed")
    return await call_next(request)

app.include_router(app_routers)

# app.add_middleware(WrapResponseMiddleware, exclude_paths={"/docs", "/redoc", "/openapi.json"})
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI"}
