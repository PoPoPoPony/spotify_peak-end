from fastapi import APIRouter
import requests
import uuid as uuidPkg
from ..models import UserInfo
from ..db_model.database import SessionLocal

router = APIRouter(
    prefix='api/v1/user',
    tags = ["for user init DB data"]
)

db = SessionLocal()


@router.post("/initUser", response_model=UserInfo)
def initUser(User: UserInfo):
    newUser = UserInfo(
        UserID = User.userID,
        UserName = User.userName,
        betweenType = User.betweenType,
        withinType = User.withinType
    )

    db.add(newUser)
    db.commit()

    return newUser