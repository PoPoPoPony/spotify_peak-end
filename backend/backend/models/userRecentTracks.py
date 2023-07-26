from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List

class UserRecentTrack(BaseModel):
    userID: UUID = Field(default_factory=uuid4)
    trackID: str
    times: int


    class Config:
        orm_mode=True


class UserRecentTracks(BaseModel):
    userID: UUID = Field(default_factory=uuid4)
    trackIDs: List[str]
    times: List[int]


    class Config:
        orm_mode=True