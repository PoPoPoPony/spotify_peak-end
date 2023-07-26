from fastapi import APIRouter
import requests
import uuid
from ..models.userSavedTracks import UserSavedTracks
from ..db_model.database import SessionLocal
from ..db_model.models import DBUserSavedTracks
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import json


router = APIRouter(
    prefix='/api/v1/userSavedTracks',
    tags = ["userSavedTracks"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateUserSavedTracks")
def updateUserSavedTracks(SavedTracks: UserSavedTracks, db: Session = Depends(get_db)):
    saved_track_ids = SavedTracks.trackIDs.split(",")
    for saved_track_id in saved_track_ids:
        DB_SavedTrack = db.query(DBUserSavedTracks).filter(DBUserSavedTracks.userID == SavedTracks.userID, DBUserSavedTracks.trackID == saved_track_id).first()
        
        if not DB_SavedTrack:
            newSavedTrack = DBUserSavedTracks(
                userID = SavedTracks.userID,
                trackID = saved_track_id,
            )

            db.add(newSavedTrack)
    db.commit()


@router.get("/checkUserExist")
def checkUserExist(userID: str, db: Session = Depends(get_db)):
    userID = uuid.UUID(userID)
    DB_User = db.query(DBUserSavedTracks).filter(DBUserSavedTracks.userID == userID).first()
    
    if DB_User:
        return True
    else:
        return False