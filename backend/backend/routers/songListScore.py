from fastapi import APIRouter
import requests
import uuid
from ..models.songListScore import SongListScore
from ..db_model.database import SessionLocal
from ..db_model.models import DBSongListScore
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


router = APIRouter(
    prefix='/api/v1/songListScore',
    tags = ["for songListScore init DB data"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateSongListScore", response_model=SongListScore)
def updateSongListScore(list_score: SongListScore, db: Session = Depends(get_db)):
    DB_list_score = db.query(DBSongListScore).filter(DBSongListScore.songListID == list_score.songListID).first()

    if not DB_list_score:
        newListScore = DBSongListScore(
            songListID = list_score.songListID,
            score = list_score.score,
        )

        db.add(newListScore)
        db.commit()
        db.refresh(newListScore)

        return newListScore
    else:
        return DBSongListScore