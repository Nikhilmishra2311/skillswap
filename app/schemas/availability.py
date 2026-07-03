from pydantic import BaseModel

class AvailabilityCreate(BaseModel):

    day: str

    start_time: str

    end_time: str