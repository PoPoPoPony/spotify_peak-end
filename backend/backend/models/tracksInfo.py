from pydantic import BaseModel, Field


class TracksInfo(BaseModel):
    trackID: str
    trackName: str
    artistID: str
    popularity: int
    acousticness: float
    danceability: float
    energy: float
    instrumentalness:float
    key:int
    liveness:float
    loudness:float
    mode:int
    speechiness:float
    tempo:float
    timeSignature:int
    valence:float
    preview:str = None

    class Config:
        orm_mode=True

# tracksInfos -> {"trackID": {"trackName": name, ...}}
class TracksInfos(BaseModel):
    tracksInfos: str

    class Config:
        orm_mode=True