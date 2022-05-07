from pydantic import BaseModel, Field
from uuid import UUID, uuid4


class AudioFeatures(BaseModel):
    userID: UUID = Field(default_factory=uuid4)
    minAcousticness: float
    targetAcousticness: float
    maxAcousticness: float
    minDanceability: float
    targetDanceability: float
    maxDanceability: float
    minEnergy: float
    targetEnergy: float
    maxEnergy: float
    minInstrumentalness: float
    targetInstrumentalness: float
    maxInstrumentalness: float
    minKey: int
    targetKey: int
    maxKey: int
    minLiveness: float
    targetLiveness: float
    maxLiveness: float
    minTempo: float
    targetTempo: float
    maxTempo: float
    minValence:float
    targetValence: float
    maxValence: float


    class Config:
        orm_mode=True