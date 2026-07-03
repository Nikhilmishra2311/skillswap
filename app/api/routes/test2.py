from fastapi import APIRouter

from app.tasks.email_tasks import welcome_email_task

router = APIRouter(
    prefix="/test",
    tags=["Testing"]
)

@router.get("/email")
def test_email():

    welcome_email_task.delay(
        "mishranikhil2311@gmail.com"   # 👈 apna Gmail likho
    )

    return {
        "message": "Email queued successfully."
    }