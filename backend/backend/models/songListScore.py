from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class SongListScore(BaseModel):
    songListID: UUID = Field(default_factory=uuid4)
    userID: UUID = Field(default_factory=uuid4)
    satisfyScore:int
    diversityScore:int
    noveltyScore:int



    class Config:
        orm_mode=True