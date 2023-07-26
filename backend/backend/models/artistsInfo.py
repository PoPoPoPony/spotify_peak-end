from pydantic import BaseModel, Field


class ArtistsInfo(BaseModel):
    artistID: str
    artistName: str
    popularity: int
    genres: str

    class Config:
        orm_mode=True

# artistInfos -> {"artistID": {"artistName": name, "popularity": p, "genres": g}}
class ArtistsInfos(BaseModel):
    artistInfos:str

    class Config:
        orm_mode=True