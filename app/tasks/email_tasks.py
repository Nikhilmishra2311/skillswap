from app.tasks.celery_app import celery
from app.services.email_service import (
    send_welcome_email,
    send_reset_password_email,
    send_session_booked_email,
    send_session_completed_email,
    send_session_reminder_email,
    send_tutor_verified_email
)


# ==========================================
# Welcome Email
# ==========================================

@celery.task(bind=True, max_retries=3)
def welcome_email_task(
    self,
    email: str,
    receiver_name: str
):

    try:

        print(f"Sending Welcome Email -> {email}")

        send_welcome_email(
            email,
            receiver_name
        )

        print("Welcome Email Sent")

        return "Welcome Email Sent"

    except Exception as e:

        print(e)

        raise self.retry(
            exc=e,
            countdown=10
        )


# ==========================================
# Forgot Password
# ==========================================

@celery.task(bind=True, max_retries=3)
def reset_password_email_task(
    self,
    email: str,
    token: str
):

    try:

        print(f"Sending Reset Password Email -> {email}")

        send_reset_password_email(
            email,
            token
        )

        print("Reset Password Email Sent")

        return "Reset Password Email Sent"

    except Exception as e:

        print(e)

        raise self.retry(
            exc=e,
            countdown=10
        )


# ==========================================
# Session Booked
# ==========================================

@celery.task(bind=True, max_retries=3)
def session_booked_email_task(
    self,
    email: str,
    receiver_name: str,
    other_person_name: str,
    topic: str,
    session_time: str
):

    try:

        print(f"Sending Session Booked Email -> {email}")

        send_session_booked_email(
            email,
            receiver_name,
            other_person_name,
            topic,
            session_time
        )

        print("Session Booked Email Sent")

        return "Session Booked Email Sent"

    except Exception as e:

        print(e)

        raise self.retry(
            exc=e,
            countdown=10
        )


# ==========================================
# Session Completed
# ==========================================

@celery.task(bind=True, max_retries=3)
def session_completed_email_task(
    self,
    email: str,
    receiver_name: str,
    topic: str,
    tokens: int
):

    try:

        print(f"Sending Session Completed Email -> {email}")

        send_session_completed_email(
            email,
            receiver_name,
            topic,
            tokens
        )

        print("Session Completed Email Sent")

        return "Session Completed Email Sent"

    except Exception as e:

        print(e)

        raise self.retry(
            exc=e,
            countdown=10
        )


# ==========================================
# Session Reminder
# ==========================================

@celery.task(bind=True, max_retries=3)
def session_reminder_email_task(
    self,
    email: str,
    receiver_name: str,
    topic: str,
    session_time: str
):

    try:

        print(f"Sending Reminder Email -> {email}")

        send_session_reminder_email(
            email,
            receiver_name,
            topic,
            session_time
        )

        print("Reminder Email Sent")

        return "Reminder Email Sent"

    except Exception as e:

        print(e)

        raise self.retry(
            exc=e,
            countdown=10
        )


# ==========================================
# Tutor Verification
# ==========================================

@celery.task(bind=True, max_retries=3)
def tutor_verified_email_task(
    self,
    email: str,
    receiver_name: str,
    topic: str
):

    try:

        print(f"Sending Tutor Verification Email -> {email}")

        send_tutor_verified_email(
            email,
            receiver_name,
            topic
        )

        print("Tutor Verification Email Sent")

        return "Tutor Verification Email Sent"

    except Exception as e:

        print(e)

        raise self.retry(
            exc=e,
            countdown=10
        )