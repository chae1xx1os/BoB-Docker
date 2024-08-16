from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    user_id: str

class AccessRequest(BaseModel):
    user_id: str
    access_id: str
    channel_id: str

class User_Data(BaseModel):
    class Config:
        orm_mode = True
        
class IoC_Data(BaseModel):
    ioc_item: Optional[str] = None
    ioc_type: Optional[str] = None

    class Config:
        orm_mode = True
