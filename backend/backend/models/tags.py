from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class Tags(BaseModel):
    userID: UUID = Field(default_factory=uuid4)
    tagID: str
    tagType: str
    tagFreq: int
    order: int
    tagSelected: bool

    class Config:
        orm_mode=True