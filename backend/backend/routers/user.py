from ctypes.wintypes import INT
from fastapi import APIRouter, Query
import requests
import uuid as uuidPkg
from ..models.user import UserInfo
from ..db_model.database import SessionLocal
from ..db_model.models import DBUserInfo
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Union


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
        withinType = User.withinType,
        secondaryType = User.secondaryType
    )

    db.add(newUser)
    db.commit()

    return newUser


@router.get("/getUser", response_model=UserInfo)
def getUser(email: str, db: Session = Depends(get_db)):
    DB_User = db.query(DBUserInfo).filter(DBUserInfo.userEmail == email).first()
    if DB_User:
        return DB_User
    else:
        return None

@router.get("/getAllUser")
def getAllUser(db: Session = Depends(get_db)):
    DB_User = db.query(DBUserInfo).all()
    return DB_User


@router.get("/getUsers")
def getUsers(expTypes: Union[List[str], None] = Query(default=None), db: Session = Depends(get_db)):
    expTypes = [x.split('_') for x in expTypes]
    retv = []
    for expType in expTypes:
        DB_User = db.query(DBUserInfo).filter(DBUserInfo.betweenType == expType[0], DBUserInfo.withinType == expType[1]).all()
        retv.extend(DB_User)

    if len(retv)>0:
        return retv
    else:
        return None