import uuid

from app.core.config import settings

from app.schemas.meeting import MeetingResponse


# =====================================
# Generate Jitsi Meeting
# =====================================

def generate_meeting(
    tutor_id: int,
    learner_id: int,
    session_id: int
) -> MeetingResponse:

    # ---------------------------------
    # Random Room ID
    # ---------------------------------

    room_id = uuid.uuid4().hex[:10]

    # ---------------------------------
    # Room Name
    # ---------------------------------

    room_name = (
        f"skillswap-"
        f"{session_id}-"
        f"{tutor_id}-"
        f"{learner_id}-"
        f"{room_id}"
    )

    # ---------------------------------
    # Meeting Link
    # ---------------------------------

    meeting_link = (
        f"{settings.JITSI_BASE_URL}/{room_name}"
    )

    return MeetingResponse(

        room_id=room_id,

        room_name=room_name,

        meeting_link=meeting_link

    )