from fastapi import APIRouter
import requests
import uuid
from ..models.songListInfo import SongListInfo
from ..db_model.database import SessionLocal
from ..db_model.models import DBSongListInfo
from ..db_model.models import DBUserInfo
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


router = APIRouter(
    prefix='/api/v1/songListInfo',
    tags = ["for songList init DB data"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateSongListInfo", response_model=SongListInfo)
def updateSongListInfo(userID: str, listType: str, db: Session = Depends(get_db)):
    userID = uuid.UUID(userID)
    DB_songList = db.query(DBSongListInfo).filter(DBSongListInfo.userID == userID, DBSongListInfo.listType == listType).first()

    if not DB_songList:
        songListID = uuid.uuid4()

        newSongList = DBSongListInfo(
            songListID = songListID,
            userID = userID,
            listType = listType
        )

        db.add(newSongList)
        db.commit()
        db.refresh(newSongList)

        return newSongList
    else:
        return DB_songList


@router.get("/getSongListInfo")
def getSongListInfo(userID: str, listType: str, db: Session = Depends(get_db)):
    userID = uuid.UUID(userID)
    DB_songList = db.query(DBSongListInfo).filter(DBSongListInfo.userID == userID, DBSongListInfo.listType == listType).first()

    if DB_songList:
        return {"songListID": DB_songList.songListID}
    else:
        return None