from fastapi import APIRouter
import requests
import uuid as uuidPkg
from ..models.tracksInfo import TracksInfo
from ..db_model.database import SessionLocal
from ..db_model.models import DBTracksInfo
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


router = APIRouter(
    prefix='/api/v1/trackInfo',
    tags = ["for trackInfo init DB data"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateTrackInfo", response_model=TracksInfo)
def updateTrackInfo(Track: TracksInfo, db: Session = Depends(get_db)):
    DB_track = db.query(DBTracksInfo).filter(DBTracksInfo.trackID == Track.trackID).first()

    if not DB_track:
        newTrack = DBTracksInfo(
            trackID = Track.trackID,
            trackName = Track.trackName,
            artistID = Track.artistID,
        )

        db.add(newTrack)
        db.commit()
        db.refresh(newTrack)

        return newTrack
    else:
        return DB_track