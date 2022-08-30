from fastapi import APIRouter
import requests
import uuid
from ..models.songListElem import SongListElem
from ..db_model.database import SessionLocal
from ..db_model.models import DBSongListElem
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


router = APIRouter(
    prefix='/api/v1/songListElem',
    tags = ["for songList init DB data"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateSongListElem", response_model=SongListElem)
def updateSongListElem(elem: SongListElem, db: Session = Depends(get_db)):
    #elem.userID = uuid.UUID(elem.userID)
    # elem.songListID = uuid.UUID(elem.songListID)

    DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == elem.songListID, DBSongListElem.trackID == elem.trackID).first()

    if not DB_songListElem:
        newSongListElem = DBSongListElem(
            songListID = elem.songListID,
            userID = elem.userID,
            trackID = elem.trackID,
            trackShowType = elem.trackShowType,
            splendidScore = elem.splendidScore,
            likeScore = elem.likeScore,
            addSongList = elem.addSongList,
            order = elem.order,
        )

        db.add(newSongListElem)
        db.commit()
        db.refresh(newSongListElem)

        return newSongListElem
    else:
        DB_songListElem.songListID = elem.songListID
        DB_songListElem.userID = elem.userID
        DB_songListElem.trackID = elem.trackID
        DB_songListElem.trackShowType = elem.trackShowType
        DB_songListElem.splendidScore = elem.splendidScore
        DB_songListElem.likeScore = elem.likeScore
        DB_songListElem.addSongList = elem.addSongList
        DB_songListElem.order = elem.order

        db.commit()
        db.refresh(DB_songListElem)

        return DB_songListElem


@router.get("/getSongListElem")
def updateSongListElem(songListID: str, db: Session = Depends(get_db)):
    DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID, DBSongListElem.trackShowType=='onList').all()

    if DB_songListElem:
        return {"trackIDsStr": ','.join([x.trackID for x in DB_songListElem])}
    
    else:
        return None