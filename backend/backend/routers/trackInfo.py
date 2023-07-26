from fastapi import APIRouter, Query
import requests
import uuid as uuidPkg
from ..models.tracksInfo import TracksInfo, TracksInfos
from ..db_model.database import SessionLocal
from ..db_model.models import DBTracksInfo
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Union
import json


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
            popularity = Track.popularity,
            acousticness = Track.acousticness,
            danceability = Track.danceability,
            energy = Track.energy,
            instrumentalness = Track.instrumentalness,
            key = Track.key,
            liveness = Track.liveness,
            loudness = Track.loudness,
            mode = Track.mode,
            speechiness = Track.speechiness,
            tempo = Track.tempo,
            timeSignature = Track.timeSignature,
            valence = Track.valence,
            preview = Track.preview
        )

        db.add(newTrack)
        db.commit()
        db.refresh(newTrack)

        return newTrack
    else:
        return DB_track



@router.post("/updateTrackInfos")
def updateTrackInfos(Infos: TracksInfos, db: Session = Depends(get_db)):
    info_dict = json.loads(Infos.tracksInfos)
    for trackID, data in info_dict.items():
        DB_track = db.query(DBTracksInfo).filter(DBTracksInfo.trackID == trackID).first()

        if not DB_track:
            newTrack = DBTracksInfo(
                trackID = trackID,
                trackName = data['trackName'],
                artistID = data['artistID'],
                popularity = data['popularity'],
                acousticness = data['acousticness'],
                danceability = data['danceability'],
                energy = data['energy'],
                instrumentalness = data['instrumentalness'],
                key = data['key'],
                liveness = data['liveness'],
                loudness = data['loudness'],
                mode = data['mode'],
                speechiness = data['speechiness'],
                tempo = data['tempo'],
                timeSignature = data['timeSignature'],
                valence = data['valence'],
                preview = data['preview']
            )

            db.add(newTrack)
    db.commit()


# Union[List[str], None] = Query(default=None) <- 接受[str1, str2, ...]
@router.get("/getTrackInfos")
def getTrackInfos(trackIDs: str, db: Session = Depends(get_db)):
    trackIDs = trackIDs.split(',')
    DB_tracks = db.query(DBTracksInfo).filter(DBTracksInfo.trackID.in_(trackIDs)).all()

    return DB_tracks


@router.get("/getTrackInfo")
def getTrackInfo(trackID: str, db: Session = Depends(get_db)):
    DB_track = db.query(DBTracksInfo).filter(DBTracksInfo.trackID==trackID).first()

    return DB_track