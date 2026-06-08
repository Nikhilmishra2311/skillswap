from fastapi import APIRouter
from app.api.routes import auth, search, sessions, test, users
from app.api.routes import skills, topics, user_skills, profile

api_router = APIRouter()


api_router.include_router(skills.router)
api_router.include_router(topics.router)
api_router.include_router(user_skills.router)
api_router.include_router(auth.router)
api_router.include_router(profile.router)
api_router.include_router(users.router)
api_router.include_router(search.router)
api_router.include_router(test.router)
api_router.include_router(sessions.router)
