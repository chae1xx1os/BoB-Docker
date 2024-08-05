from pydantic import BaseModel

class UserCreate(BaseModel):
    user_id: str

class AccessRequest(BaseModel):
    access_id: str
    user_id: str
    channel_id: str
