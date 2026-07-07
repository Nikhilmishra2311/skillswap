import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.config import settings


def send_email(
    to_email: str,
    subject: str,
    body: str
):

    message = MIMEMultipart()

    message["From"] = settings.EMAIL_FROM
    message["To"] = to_email
    message["Subject"] = subject

    message.attach(
        MIMEText(
            body,
            "html"
        )
    )

    server = smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT
    )

    server.starttls()

    server.login(
        settings.SMTP_USERNAME,
        settings.SMTP_PASSWORD
    )

    try:

        server.send_message(message)

        print(f"✅ Email sent to {to_email}")

    except Exception as e:

        print(f"❌ Email Error : {e}")

        raise

    finally:

        server.quit()


# ==========================================
# Welcome Email
# ==========================================

def send_welcome_email(
    email: str,
    username: str
):

    body = f"""
<html>

<body>

<h2>Welcome to SkillSwap 🎉</h2>

<p>Hello <b>{username}</b>,</p>

<p>
Thank you for joining SkillSwap.
</p>

<p>
Your username is:
<b>@{username}</b>
</p>

<p>
Start learning and teaching today.
</p>

</body>

</html>
"""

    send_email(
        email,
        "Welcome to SkillSwap",
        body
    )


# ==========================================
# Forgot Password
# ==========================================

def send_reset_password_email(
    email: str,
    token: str
):

    body = f"""
    <html>

    <body>

        <h2>Password Reset</h2>

        <p>

        Use the following token to reset password.

        </p>

        <h3>{token}</h3>

    </body>

    </html>
    """

    send_email(
        email,
        "Reset Password",
        body
    )


# ==========================================
# Session Booked
# ==========================================

def send_session_booked_email(

    email: str,
    receiver_name: str,
    other_person: str,
    topic: str,
    session_time: str,
    meeting_link: str

):

    body = f"""
<html>

<body>

<h2>📚 Session Booked Successfully</h2>

<p>Hello <b>{receiver_name}</b>,</p>

<p>
Your session with
<b>{other_person}</b>
has been booked successfully.
</p>

<p>
<b>Topic :</b> {topic}
</p>

<p>
<b>Time :</b> {session_time}
</p>

<p>
<b>Meeting Link :</b>
</p>

<p>
<a href="{meeting_link}">
{meeting_link}
</a>
</p>

<p>
Click the above link at the scheduled time to join the video session.
</p>

</body>

</html>
"""

    send_email(
        email,
        "Session Booked",
        body
    )

# ==========================================
# Session Completed
# ==========================================

def send_session_completed_email(

    email: str,

    receiver_name: str,

    topic: str,

    tokens: int

):

    body = f"""
<html>

<body>

<h2>🎉 Session Completed</h2>

<p>Hello <b>{receiver_name}</b>,</p>

<p>
Your session on
<b>{topic}</b>
has been completed successfully.
</p>

<p>
Tokens Earned :
<b>{tokens}</b>
</p>

<p>
Keep learning on SkillSwap 🚀
</p>

</body>

</html>
"""

    send_email(
        email,
        "Session Completed",
        body
    )


# ==========================================
# Session Reminder
# ==========================================

def send_session_reminder_email(

    email: str,
    receiver_name: str,
    topic: str,
    session_time: str,
    meeting_link: str

):

    body = f"""
<html>

<body>

<h2>⏰ Session Reminder</h2>

<p>Hello <b>{receiver_name}</b>,</p>

<p>
Your <b>{topic}</b> session starts at
<b>{session_time}</b>.
</p>

<p>
<b>Join Meeting</b>
</p>

<p>
<a href="{meeting_link}">
{meeting_link}
</a>
</p>

<p>
Please join 5 minutes before the session starts.
</p>

</body>

</html>
"""

    send_email(
        email,
        "Session Reminder",
        body
    )
# ==========================================
# Tutor Verification
# ==========================================

def send_tutor_verified_email(

    email: str,

    receiver_name: str,

    topic: str

):
    body = f"""
<html>

<body>

<h2>🎉 Congratulations</h2>

<p>Hello <b>{receiver_name}</b>,</p>

<p>
Your tutor profile for

<b>{topic}</b>

has been verified.

</p>

<p>
You can now start teaching on SkillSwap.
</p>

</body>

</html>
"""

    send_email(
        email,
        "Tutor Verified",
        body
    )