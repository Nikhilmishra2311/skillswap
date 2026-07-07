from pydantic import BaseModel


class MeetingResponse(BaseModel):

    room_id: str

    room_name: str

    meeting_link: str