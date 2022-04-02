from pydantic import BaseModel
from uuid import UUID


class UserInfo(BaseModel):
    userID: UUID
    userName: str
    betweenType: int
    withinType: int

    class Config:
        orm_mode=True