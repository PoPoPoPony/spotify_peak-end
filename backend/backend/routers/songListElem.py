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
            splendidScore = elem.splendidScore,
            likeScore = elem.likeScore,
            addSongList = elem.addSongList,
            order = elem.order,
            beforeListened = elem.beforeListened,
            recommend = elem.recommend
        )

        db.add(newSongListElem)
        db.commit()
        db.refresh(newSongListElem)

        return newSongListElem
    else:
        DB_songListElem.songListID = elem.songListID
        DB_songListElem.userID = elem.userID
        DB_songListElem.trackID = elem.trackID
        DB_songListElem.splendidScore = elem.splendidScore
        DB_songListElem.likeScore = elem.likeScore
        DB_songListElem.addSongList = elem.addSongList
        DB_songListElem.order = elem.order
        DB_songListElem.beforeListened = elem.beforeListened

        db.commit()
        db.refresh(DB_songListElem)

        return DB_songListElem


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


@router.get("/getSongListElem")
# order : 0: ascending, 1: descending, other: ignore
def getSongListElem(songListID: str, order: int, db: Session = Depends(get_db)):
    if order == 0:
        DB_songListElem = db.query(DBSongListElem.trackID).filter(DBSongListElem.songListID == songListID).order_by(DBSongListElem.likeScore.asc()).all()
    elif order == 1:
        DB_songListElem = db.query(DBSongListElem.trackID).filter(DBSongListElem.songListID == songListID).order_by(DBSongListElem.likeScore.desc()).all()
    else:
        DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID).all()

    if DB_songListElem:
        return {"trackIDsStr": ','.join([x[0] for x in DB_songListElem])}
    else:
        return None


@router.get("/getElemByRule")
# 目前暫定計分方式 : 只看like
def getElemByRule(songListID: str, ruleType:str, num: int, order:int, db: Session = Depends(get_db)):
    DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID).all()

    # 除order之外皆是舊的code，不知道在寫三小
    #  0718 改寫like (Analyze那邊可能有用到需再修正)
    # rulType : like、dislike、end
    # order : 0: ascending, 1: descending, other: ignore
    if ruleType=='like_original':
        likeScores = [x.likeScore for x in DB_songListElem]
        likeScores.sort(reverse=True)
        return likeScores[:num]

    elif ruleType=='dislike':
        likeScores = [x.likeScore for x in DB_songListElem]
        likeScores.sort()
        return likeScores[:num]
    elif ruleType=='end':
        DB_songListElem.sort(key=lambda x: x.order)
        likeScores = [x.likeScore for x in DB_songListElem]
        return likeScores[-num:]
    elif ruleType=='order':
        if order == 0:
            elems = sorted(DB_songListElem, key=lambda x:x.order)
        elif order == 1:
            elems = sorted(DB_songListElem, key=lambda x:x.order, reverse=True)
        else:
            elems = sorted(DB_songListElem, key=lambda x:x.order)
        return elems[:num]
    elif ruleType=='like':
        if order == 0:
            elems = sorted(DB_songListElem, key=lambda x:x.likeScore)
        elif order == 1:
            elems = sorted(DB_songListElem, key=lambda x:x.likeScore, reverse=True)
        else:
            elems = sorted(DB_songListElem, key=lambda x:x.likeScore)

        return elems[:num]



@router.get("/getAllSongs")
def getAllSongs(songListID: str, containDelete:bool, db: Session = Depends(get_db)):
    if containDelete:
        DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID).all()
    else:
        DB_songListElem = db.query(DBSongListElem).filter(DBSongListElem.songListID == songListID, DBSongListElem.trackShowType=='onList').all()

    return DB_songListElem