from pydantic import BaseModel, Field


class Artists(BaseModel):
    artistID: str
    artistName: str

    class Config:
        orm_mode=True