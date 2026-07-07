from pydantic import BaseModel


# =====================================
# Create Availability
# =====================================

class AvailabilityCreate(BaseModel):

    day: str

    start_time: str

    end_time: str


# =====================================
# Update Availability
# =====================================

class UpdateAvailability(BaseModel):

    day: str

    start_time: str

    end_time: str