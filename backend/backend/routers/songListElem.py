from fastapi import APIRouter
import requests
import uuid
from ..models.songListElem import SongListElem, SongListElems
from ..db_model.database import SessionLocal
from ..db_model.models import DBSongListElem
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


router = APIRouter(
    prefix='/api/v1/songListElem',
    tags = ["SongListElem"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()

# [deprecate]
# @router.post("/updateSongListElem", response_model=SongListElem)
# def updateSongListElem(elem: SongListElem, db: Session = Depends(get_db)):
#     #elem.userID = uuid.UUID(elem.userID)
#     # elem.songListID = uuid.UUID(elem.songListID)

#     DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == elem.songListID, DBSongListElem.trackID == elem.trackID).first()

#     if not DB_songListElem:
#         newSongListElem = DBSongListElem(
#             songListID = elem.songListID,
#             userID = elem.userID,
#             trackID = elem.trackID,
#             splendidScore = elem.splendidScore,
#             likeScore = elem.likeScore,
#             addSongList = elem.addSongList,
#             order = elem.order,
#             beforeListened = elem.beforeListened,
#             recommend = elem.recommend
#         )

#         db.add(newSongListElem)
#         db.commit()
#         db.refresh(newSongListElem)

#         return newSongListElem
#     else:
#         DB_songListElem.songListID = elem.songListID
#         DB_songListElem.userID = elem.userID
#         DB_songListElem.trackID = elem.trackID
#         DB_songListElem.splendidScore = elem.splendidScore
#         DB_songListElem.likeScore = elem.likeScore
#         DB_songListElem.addSongList = elem.addSongList
#         DB_songListElem.order = elem.order
#         DB_songListElem.beforeListened = elem.beforeListened

#         db.commit()
#         db.refresh(DB_songListElem)

#         return DB_songListElem


@router.post("/updateSongListElems")
def updateSongListElems(elems: SongListElems, db: Session = Depends(get_db)):
    for song_list_elem in elems.elems:
        DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == song_list_elem.songListID, DBSongListElem.trackID == song_list_elem.trackID).first()

        if not DB_songListElem:
            newSongListElem = DBSongListElem(
                songListID = song_list_elem.songListID,
                userID = song_list_elem.userID,
                trackID = song_list_elem.trackID,
                splendidScore = song_list_elem.splendidScore,
                likeScore = song_list_elem.likeScore,
                addSongList = song_list_elem.addSongList,
                order = song_list_elem.order,
                beforeListened = song_list_elem.beforeListened,
                recommend = song_list_elem.recommend
            )

            db.add(newSongListElem)
            db.commit()
            db.refresh(newSongListElem)



@router.get("/getSongListElems")
# order : 0: ascending, 1: descending, other: ignore
# ruleType must be the column of the SongListElem
def getSongListElems(songListID: str, ruleType: str, order: int, db: Session = Depends(get_db)):
    col_names = [x for x in DBSongListElem.__dict__ if '_' not in x]
    if ruleType not in col_names:
        return None
    if order == 0:
        DB_songListElems = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID).order_by(DBSongListElem.__dict__[ruleType].asc()).all()
    elif order == 1:
        DB_songListElems = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID).order_by(DBSongListElem.__dict__[ruleType].desc()).all()
    else:
        DB_songListElems = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID).all()

    if DB_songListElems:
        return DB_songListElems
    else:
        return None