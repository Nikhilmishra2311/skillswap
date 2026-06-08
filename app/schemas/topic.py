from pydantic import BaseModel

class TopicCreate(BaseModel):
    name: str