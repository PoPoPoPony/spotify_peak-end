from pydantic import BaseModel, Field


class TracksInfo(BaseModel):
    trackID: str
    trackName: str
    artistID: str

    class Config:
        orm_mode=True