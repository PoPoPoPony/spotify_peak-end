from fastapi import APIRouter
import requests
import uuid as uuidPkg
from ..models.tags import Tags
from ..db_model.database import SessionLocal
from ..db_model.models import DBTags
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


router = APIRouter(
    prefix='/api/v1/tags',
    tags = ["for tags init DB data"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.post("/updateTags", response_model=Tags)
def updateTrackInfo(tag: Tags, db: Session = Depends(get_db)):
    DB_tag = db.query(DBTags).filter(DBTags.userID == tag.userID, DBTags.tagID == tag.tagID).first()

    if not DB_tag:
        newTag = DBTags(
            userID = tag.userID, 
            tagID = tag.tagID,
            tagType = tag.tagType,
            tagFreq = tag.tagFreq,
            order = tag.order,
            tagSelected = tag.tagSelected,
        )

        db.add(newTag)
        db.commit()
        db.refresh(newTag)

        return newTag
    else:
        return DB_tag



@router.get("/getAllTags",)
def getAllTags(userID: str, db: Session = Depends(get_db)):
    DB_tags = db.query(DBTags).filter(DBTags.userID == userID).all()

    return DB_tags