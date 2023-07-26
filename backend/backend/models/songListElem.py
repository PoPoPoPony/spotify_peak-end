from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List


class SongListElem(BaseModel):
    songListID: UUID = Field(default_factory=uuid4)
    userID: UUID = Field(default_factory=uuid4)
    trackID: str
    splendidScore: int
    likeScore: int
    addSongList: bool
    order: int
    beforeListened: bool
    recommend: str

    class Config:
        orm_mode=True


class SongListElems(BaseModel):
    elems: List[SongListElem]

    class Config:
        orm_mode=True