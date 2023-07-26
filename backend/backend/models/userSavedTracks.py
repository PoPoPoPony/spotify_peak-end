from pydantic import BaseModel, Field
from uuid import UUID, uuid4

# trackIDs -> ID1,ID2,ID3,...
class UserSavedTracks(BaseModel):
    userID: UUID = Field(default_factory=uuid4)
    trackIDs: str


    class Config:
        orm_mode=True