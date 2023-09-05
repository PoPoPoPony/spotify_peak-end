from fastapi import APIRouter, Query
import requests
import uuid as uuidPkg
from ..models.artistsInfo import ArtistsInfo, ArtistsInfos
from ..db_model.database import SessionLocal
from ..db_model.models import DBArtistsInfo
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Union
import json

router = APIRouter(
    prefix='/api/v1/artistInfo',
    tags = ["ArtistInfo"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

# [deprecate]
# @router.post("/updateArtistInfo", response_model=ArtistsInfo)
# def updateArtistInfo(Artist: ArtistsInfo, db: Session = Depends(get_db)):
#     DB_artist = db.query(DBArtistsInfo).filter(DBArtistsInfo.artistID == Artist.artistID).first()

#     if not DB_artist:
#         newArtist = DBArtistsInfo(
#             artistID = Artist.artistID,
#             artistName = Artist.artistName,
#             popularity = Artist.popularity,
#             genres = Artist.genres
#         )

#         db.add(newArtist)
#         db.commit()
#         db.refresh(newArtist)

#         return newArtist
#     else:
#         return DB_artist


@router.post("/updateArtistInfos")
def updateArtistInfos(Infos: ArtistsInfos, db: Session = Depends(get_db)):
    info_dict = json.loads(Infos.artistInfos)
    for artistID, data in info_dict.items():
        DB_artist = db.query(DBArtistsInfo).filter(DBArtistsInfo.artistID == artistID).first()
        if not DB_artist:
            newArtist = DBArtistsInfo(
                artistID = artistID,
                artistName = data['artistName'],
                popularity = data['popularity'],
                genres = data['genres']
            )
            try:
                db.add(newArtist)
                db.commit()
                db.refresh(newArtist)
            except Exception as e:
                continue



@router.get("/getArtistInfos")
def getArtistInfos(artistIDs: Union[List[str], None] = Query(default=None), db: Session = Depends(get_db)):
    DB_artists = []
    for artistID in artistIDs:
        DB_artists.append(db.query(DBArtistsInfo).filter(DBArtistsInfo.artistID == artistID).first())


    return DB_artists



# [deprecate]
# @router.get("/getArtistInfo")
# def getArtistInfo(artistID: str, db: Session = Depends(get_db)):
#     DB_artist = db.query(DBArtistsInfo).filter(DBArtistsInfo.artistID==artistID).first()

#     return DB_artist