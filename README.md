# SkillSwap Backend

A peer-to-peer learning platform backend built using FastAPI.

## Features

* User Authentication (JWT)
* User Profiles
* Skill Management
* User Skill Mapping
* Session Booking
* Skill Assessment Tests
* Search & Matching
* Alembic Database Migrations

## Tech Stack

* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* JWT Authentication
* Pydantic

## Project Structure

app/
├── api/
├── core/
├── db/
├── models/
├── schemas/
├── services/
└── main.py

## Installation

1. Clone the repository

git clone <repository-url>

2. Create virtual environment

python -m venv .venv

3. Activate virtual environment

Windows:
.venv\Scripts\activate

4. Install dependencies

pip install -r requirements.txt

5. Run the server

uvicorn app.main:app --reload

## Future Enhancements

* Redis Caching
* WebSocket Chat
* AI-based Skill Matching
* Docker Deployment
* Microservice Architecture
