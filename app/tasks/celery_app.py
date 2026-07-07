from celery import Celery
from celery.schedules import crontab

from app.core.config import settings


celery = Celery(

    "skillswap",

    broker=settings.CELERY_BROKER_URL,

    backend=settings.CELERY_RESULT_BACKEND,

    include=[
        "app.tasks.email_tasks",
        "app.tasks.notification_tasks",
        "app.tasks.session_tasks"
    ]

)

celery.conf.update(

    task_serializer="json",

    result_serializer="json",

    accept_content=["json"],

    timezone="UTC",

    enable_utc=True,

    task_track_started=True,

    result_expires=3600,

    beat_schedule={

        # ==========================================
        # Every Minute
        # ==========================================

        "expire-sessions":{

            "task":"app.tasks.session_tasks.expire_sessions",

            "schedule":60.0

        },

        # ==========================================
        # Every 5 Minutes
        # ==========================================

        "session-reminders":{

            "task":"app.tasks.session_tasks.send_session_reminders",

            "schedule":300.0

        },

        # ==========================================
        # Every Day 3 AM
        # ==========================================

        "cleanup-old-sessions":{

            "task":"app.tasks.session_tasks.cleanup_old_sessions",

            "schedule":crontab(

                hour=3,

                minute=0

            )

        }

    }

)