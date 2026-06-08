from fastapi import FastAPI
from app.api.router import api_router
from app.db.init_db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "SkillSwap Running 🚀"}