from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class UserInfo(BaseModel):
    userID: UUID = Field(default_factory=uuid4)
    userName: str
    betweenType: int
    withinType: int

    class Config:
        orm_mode=True