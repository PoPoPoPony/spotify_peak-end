from fastapi import APIRouter, Query
import requests
import uuid as uuidPkg
from ..models.artists import Artists
from ..db_model.database import SessionLocal
from ..db_model.models import DBArtists
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Union

router = APIRouter(
    prefix='/api/v1/artist',
    tags = ["for artist init DB data"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateArtist", response_model=Artists)
def updateArtist(Artist: Artists, db: Session = Depends(get_db)):
    DB_artist = db.query(DBArtists).filter(DBArtists.artistID == Artist.artistID).first()

    if not DB_artist:
        newArtist = DBArtists(
            artistID = Artist.artistID,
            artistName = Artist.artistName,
        )

        db.add(newArtist)
        db.commit()
        db.refresh(newArtist)

        return newArtist
    else:
        return DB_artist

@router.get("/getArtistInfos")
def getArtistInfos(artistIDs: Union[List[str], None] = Query(default=None), db: Session = Depends(get_db)):
    DB_artists = db.query(DBArtists).filter(DBArtists.artistID.in_(artistIDs)).all()

    return DB_artists


@router.get("/getArtistInfo")
def getArtistInfo(artistID: str, db: Session = Depends(get_db)):
    DB_artist = db.query(DBArtists).filter(DBArtists.artistID==artistID).first()

    return DB_artist