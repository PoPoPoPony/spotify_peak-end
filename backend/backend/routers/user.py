from fastapi import APIRouter
import requests
import uuid as uuidPkg
from ..models.user import UserInfo
from ..db_model.database import SessionLocal
from ..db_model.models import DBUserInfo
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter(
    prefix='/api/v1/user',
    tags = ["for user init DB data"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/initUser", response_model=UserInfo)
def initUser(User: UserInfo, db: Session = Depends(get_db)):
    
    newUser = DBUserInfo(
        userID = User.userID,
        userEmail = User.userEmail,
        betweenType = User.betweenType,
        withinType = User.withinType
    )

    db.add(newUser)
    db.commit()

    return newUser


@router.get("/getUser")
def getUser(email: str, db: Session = Depends(get_db)):
    DB_User = db.query(DBUserInfo).filter(DBUserInfo.userEmail == email).first()
    if DB_User:
        return {"userID": DB_User.userID}
    else:
        return None

@router.get("/getAllUser")
def getUser(db: Session = Depends(get_db)):
    DB_User = db.query(DBUserInfo).all()
    return DB_User