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
from ..routers.trackInfo import getTrackInfos
from ..routers.artistsInfo import getArtistInfos
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

# [deprecate]
# @router.post("/updateUserRecentTrack")
# def updateUserRecentTrack(RecentTrack: UserRecentTrack, db: Session = Depends(get_db)):
#     DB_RecentTrack = db.query(DBUserRecentTracks).filter(DBUserRecentTracks.userID == RecentTrack.userID, DBUserRecentTracks.trackID == RecentTrack.trackID).first()
    
#     if not DB_RecentTrack:
#         newRecentTrack = DBUserRecentTracks(
#             userID = RecentTrack.userID,
#             trackID = RecentTrack.trackID,
#             times = RecentTrack.times
#         )

#         db.add(newRecentTrack)
#         db.commit()
#         db.refresh(newRecentTrack)


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
            db.refresh(newRecentTrack)


@router.get("/checkUserExist")
def checkUserExist(userID: str, db: Session = Depends(get_db)):
    userID = uuid.UUID(userID)
    DB_User = db.query(DBUserRecentTracks).filter(DBUserRecentTracks.userID == userID).first()
    
    if DB_User:
        return True
    else:
        return False


@router.get("/getUserRecentTracks")
def getUserRecentTracks(userID: str, db: Session = Depends(get_db)):
    retv = []

    userID = uuid.UUID(userID)
    DB_RecentTracks = db.query(DBUserRecentTracks).filter(DBUserRecentTracks.userID == userID).all()

    if DB_RecentTracks:
        trackInfos = getTrackInfos([track.trackID for track in DB_RecentTracks], db)
        artistInfos = getArtistInfos([trackInfo.artistID for trackInfo in trackInfos], db)
        genres = [artistInfo.genres.split(",") if len(artistInfo.genres)>0 else [] for artistInfo in artistInfos]

        for i in range(len(DB_RecentTracks)):
            retv.append({
                'trackID': trackInfos[i].trackID,
                'times': DB_RecentTracks[i].times,
                'artistID': artistInfos[i].artistID,
                'artistName': artistInfos[i].artistName,
                'genres': genres[i],
                'trackName': trackInfos[i].trackName,
                'danceability': trackInfos[i].danceability,
                'acousticness': trackInfos[i].acousticness,
                'instrumentalness': trackInfos[i].instrumentalness,
                'energy': trackInfos[i].energy,
                'liveness': trackInfos[i].liveness,
                'key': trackInfos[i].key,
                'tempo': trackInfos[i].tempo,
                'valence': trackInfos[i].valence,
                'track_popularity': trackInfos[i].popularity,
                'artist_popularity': artistInfos[i].popularity,
                'mode': trackInfos[i].mode,
                'speechiness': trackInfos[i].speechiness,
                'time_signature': trackInfos[i].timeSignature
            })

        return retv
    else:
        return None