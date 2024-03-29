from fastapi import APIRouter
import requests
import uuid
from ..models.userAudioFeatures import UserAudioFeatures
from ..db_model.database import SessionLocal
from ..db_model.models import DBUserAudioFeatures
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import json


router = APIRouter(
    prefix='/api/v1/userAudioFeatures',
    tags = ["UserAudioFeatures"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateUserAudioFeatures", response_model=UserAudioFeatures)
def updateUserAudioFeatures(userID: uuid.UUID, score_obj: str, db: Session = Depends(get_db)):
    DB_AudioFeatures = db.query(DBUserAudioFeatures).filter(DBUserAudioFeatures.userID == userID).first()
    score_obj = json.loads(score_obj)

    audiofeatures = {}
    score_obj_keys = list(score_obj.keys())
    for i in score_obj_keys:
        newKey = i.split("_")[0] + i.split("_")[1][0].upper() + i.split("_")[1][1:]
        audiofeatures[newKey] = score_obj.pop(i)

    if not DB_AudioFeatures:
        newAudioFeatures = DBUserAudioFeatures(
            userID = userID,
            minAcousticness = audiofeatures['minAcousticness'],
            targetAcousticness = audiofeatures['targetAcousticness'],
            maxAcousticness = audiofeatures['maxAcousticness'],
            minDanceability = audiofeatures['minDanceability'],
            targetDanceability = audiofeatures['targetDanceability'],
            maxDanceability = audiofeatures['maxDanceability'],
            minEnergy = audiofeatures['minEnergy'],
            targetEnergy = audiofeatures['targetEnergy'],
            maxEnergy = audiofeatures['maxEnergy'],
            minInstrumentalness = audiofeatures['minInstrumentalness'],
            targetInstrumentalness = audiofeatures['targetInstrumentalness'],
            maxInstrumentalness = audiofeatures['maxInstrumentalness'],
            minKey = audiofeatures['minKey'],
            targetKey = audiofeatures['targetKey'],
            maxKey = audiofeatures['maxKey'],
            minLiveness = audiofeatures['minLiveness'],
            targetLiveness = audiofeatures['targetLiveness'],
            maxLiveness = audiofeatures['maxLiveness'],
            minTempo = audiofeatures['minTempo'],
            targetTempo = audiofeatures['targetTempo'],
            maxTempo = audiofeatures['maxTempo'],
            minValence = audiofeatures['minValence'],
            targetValence = audiofeatures['targetValence'],
            maxValence = audiofeatures['maxValence'],
        )

        db.add(newAudioFeatures)
        db.commit()
        db.refresh(newAudioFeatures)

        return newAudioFeatures
    else:
        return DB_AudioFeatures
    
@router.get("/getUserAudioFeatures")
def getUserAudioFeatures(userID: str, db: Session = Depends(get_db)):
    userID = uuid.UUID(userID)
    DB_UserAudioFeatures = db.query(DBUserAudioFeatures).filter(DBUserAudioFeatures.userID == userID).first()

    if DB_UserAudioFeatures:
        return DB_UserAudioFeatures
    else:
        return None