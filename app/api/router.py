from fastapi import APIRouter

from app.api.routes import (
    auth,
    search,
    sessions,
    users,
    skills,
    topics,
    user_skills,
    profile,
    token_transactions,
    matching,
    availability,
    question,
    notification,
    dashboard,
    admin,
    verification
)

from app.api.routes.test2 import router as test_router

api_router = APIRouter()

# Testing
api_router.include_router(test_router)

# Auth
api_router.include_router(auth.router)

# User
api_router.include_router(users.router)
api_router.include_router(profile.router)

# Skills
api_router.include_router(skills.router)
api_router.include_router(topics.router)
api_router.include_router(user_skills.router)

# Search
api_router.include_router(search.router)
api_router.include_router(matching.router)

# Question Bank
api_router.include_router(question.router)

# Tutor Verification
api_router.include_router(verification.router)

# Sessions
api_router.include_router(availability.router)
api_router.include_router(sessions.router)

# Tokens
api_router.include_router(token_transactions.router)

# Notifications
api_router.include_router(notification.router)

# Dashboard
api_router.include_router(dashboard.router)

# Admin
api_router.include_router(admin.router)