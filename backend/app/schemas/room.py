from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


# Shared properties
class RoomBase(BaseModel):
    name: str
    description: Optional[str] = None
    logo_url: Optional[str] = None
    website: Optional[str] = None
    is_active: bool = True


# Properties to receive on room creation
class RoomCreate(RoomBase):
    pass


# Properties to receive on room update
class RoomUpdate(RoomBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None


# Properties shared by models stored in DB
class RoomInDBBase(RoomBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class Room(RoomInDBBase):
    pass


# Properties properties stored in DB
class RoomInDB(RoomInDBBase):
    pass 