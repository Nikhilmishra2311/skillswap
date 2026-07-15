import os
from fastapi.middleware.cors import CORSMiddleware
from app.core.minio import initialize_bucket
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.limiter import limiter
from app.api.router import api_router
from app.db.init_db import init_db

app = FastAPI(

    title="SkillSwap API",

    version="1.0.0",

    description="Production Backend",

    docs_url="/docs",

    redoc_url="/redoc"

)

app.state.limiter = limiter

app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)

app.add_middleware(
    SlowAPIMiddleware
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



@app.on_event("startup")
def startup():
    initialize_bucket()
    init_db()

app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Hello,Welcome to SkillSwap a best platform for skill exchange.You can exchange skills with other users. 🚀"
        }





