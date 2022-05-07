from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class SongListInfo(BaseModel):
    songListID: UUID = Field(default_factory=uuid4)
    userID: UUID = Field(default_factory=uuid4)
    listType: str

    class Config:
        orm_mode=True