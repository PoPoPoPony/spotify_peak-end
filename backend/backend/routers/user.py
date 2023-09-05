from fastapi import APIRouter, Query, HTTPException
import requests
import uuid as uuidPkg
from ..models.user import UserInfo
from ..db_model.database import SessionLocal
from ..db_model.models import DBUserInfo
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Union
from random import choice


router = APIRouter(
    prefix='/api/v1/user',
    tags = ["User"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()




def random_sencondary_type():
    res = requests.get(url='http://ponylis.ddns.net:8080/api/v1/user/getAllUser')
    res = res.json()
    secondary = [x['secondaryType'] for x in res]
    d = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
    }
    for s in secondary:
        d[s]+=1

    candidate = []
    for group in d.keys():
        if d[group] == min(d.values()):
            candidate.append(group)

    return choice(candidate)


@router.post("/initUser")
def initUser(User: UserInfo, db: Session = Depends(get_db)):
    DB_User = db.query(DBUserInfo).filter(DBUserInfo.userID == User.userID).first()

    if not DB_User:
        newUser = DBUserInfo(
            userID = User.userID,
            userEmail = User.userEmail,
            betweenType = User.betweenType,
            withinType = User.withinType,
            secondaryType = random_sencondary_type()
        )

        db.add(newUser)
        db.commit()
        db.refresh(newUser)

        return newUser
    else:
        raise HTTPException(status_code=404, detail="userID exist!")



@router.get("/getUser")
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

# [deprecate]
# @router.get("/getUsers")
# def getUsers(expTypes: Union[List[str], None] = Query(default=None), db: Session = Depends(get_db)):
#     expTypes = [x.split('_') for x in expTypes]
#     retv = []
#     for expType in expTypes:
#         DB_User = db.query(DBUserInfo).filter(DBUserInfo.betweenType == expType[0], DBUserInfo.withinType == expType[1]).all()
#         retv.extend(DB_User)

#     if len(retv)>0:
#         return retv
#     else:
#         return None