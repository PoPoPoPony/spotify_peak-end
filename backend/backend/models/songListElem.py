from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class SongListElem(BaseModel):
    songListID: UUID = Field(default_factory=uuid4)
    userID: UUID = Field(default_factory=uuid4)
    trackID: str
    trackShowType: str
    splendidScore: int
    likeScore: int
    addSongList: bool
    order: int

    class Config:
        orm_mode=True