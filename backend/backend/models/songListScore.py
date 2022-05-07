from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class SongListScore(BaseModel):
    songListID: UUID = Field(default_factory=uuid4)
    score: int

    class Config:
        orm_mode=True