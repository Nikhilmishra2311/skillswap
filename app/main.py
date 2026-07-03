import os
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.db.init_db import init_db

app = FastAPI(

    title="SkillSwap API",

    version="1.0.0",

    description="Production Backend",

    docs_url="/docs",

    redoc_url="/redoc"

)
app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]

)



@app.on_event("startup")
def on_startup():
    init_db()

# Ensure upload folder exists before mounting static files
os.makedirs("uploads", exist_ok=True)

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "SkillSwap Running 🚀"}

app.mount(
    "/media",
    StaticFiles(directory="uploads"),
    name="media"
)