from fastapi import APIRouter, Query
import requests
import uuid
from ..models.userRecentTracks import UserRecentTrack, UserRecentTracks
from ..db_model.database import SessionLocal
from ..db_model.models import DBUserRecentTracks
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import json
from ..routers.trackInfo import getTrackInfo
from ..routers.artistsInfo import getArtistInfo
from typing import Union, List


router = APIRouter(
    prefix='/api/v1/userRecentTracks',
    tags = ["userRecentTracks"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateUserRecentTrack")
def updateUserRecentTrack(RecentTrack: UserRecentTrack, db: Session = Depends(get_db)):
    DB_RecentTrack = db.query(DBUserRecentTracks).filter(DBUserRecentTracks.userID == RecentTrack.userID, DBUserRecentTracks.trackID == RecentTrack.trackID).first()
    
    if not DB_RecentTrack:
        newRecentTrack = DBUserRecentTracks(
            userID = RecentTrack.userID,
            trackID = RecentTrack.trackID,
            times = RecentTrack.times
        )

        db.add(newRecentTrack)
        db.commit()
        # db.refresh(newRecentTrack)


@router.post("/updateUserRecentTracks")
def updateUserRecentTracks(RecentTracks: UserRecentTracks, db: Session = Depends(get_db)):
    userID = RecentTracks.userID
    trackIDs = RecentTracks.trackIDs
    times = RecentTracks.times

    for i in range(len(trackIDs)):
        DB_RecentTrack = db.query(DBUserRecentTracks).filter(DBUserRecentTracks.userID == userID, DBUserRecentTracks.trackID == trackIDs[i]).first()
        if not DB_RecentTrack:
            newRecentTrack = DBUserRecentTracks(
                userID = userID,
                trackID = trackIDs[i],
                times = times[i]
            )

            db.add(newRecentTrack)
    db.commit()
    # db.refresh(newRecentTrack)


@router.get("/checkUserExist")
def checkUserExist(userID: str, db: Session = Depends(get_db)):
    userID = uuid.UUID(userID)
    DB_User = db.query(DBUserRecentTracks).filter(DBUserRecentTracks.userID == userID).first()
    
    if DB_User:
        return True
    else:
        return False


@router.get("/getUserRecentTrack")
def getUserRecentTrack(userID: str, db: Session = Depends(get_db)):
    retv = []
    
    userID = uuid.UUID(userID)
    DB_RecentTracks = db.query(DBUserRecentTracks).filter(DBUserRecentTracks.userID == userID).all()
    
    if DB_RecentTracks:
        for track in DB_RecentTracks:
            trackInfo = getTrackInfo(track.trackID, db)
            artistInfo = getArtistInfo(trackInfo.artistID, db)
            genres = artistInfo.genres.split(",") if len(artistInfo.genres)>0 else []

            retv.append({
                'trackID': track.trackID,
                'times': track.times,
                'artistID': artistInfo.artistID,
                'artistName': artistInfo.artistName,
                'genres': genres,
                'trackName': trackInfo.trackName,
                'danceability': trackInfo.danceability,
                'acousticness': trackInfo.acousticness,
                'instrumentalness': trackInfo.instrumentalness,
                'energy': trackInfo.energy,
                'liveness': trackInfo.liveness,
                'key': trackInfo.key,
                'tempo': trackInfo.tempo,
                'valence': trackInfo.valence
            })

        return retv
    else:
        return None