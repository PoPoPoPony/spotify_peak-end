from fastapi import APIRouter
import requests
import uuid
from ..models.tags import Tags, SeveralTags
from ..db_model.database import SessionLocal
from ..db_model.models import DBTags
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status


router = APIRouter(
    prefix='/api/v1/tags',
    tags = ["Tags"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


# [deprecate]
# add one tag
# @router.post("/updateTags", response_model=Tags)
# def updateTagInfo(tag: Tags, db: Session = Depends(get_db)):
#     DB_tag = db.query(DBTags).filter(DBTags.userID == tag.userID, DBTags.tagID == tag.tagID).first()

#     if not DB_tag:
#         newTag = DBTags(
#             userID = tag.userID, 
#             tagID = tag.tagID,
#             tagType = tag.tagType,
#             tagFreq = tag.tagFreq,
#             order = tag.order,
#             tagSelected = tag.tagSelected,
#         )

#         db.add(newTag)
#         db.commit()
#         db.refresh(newTag)

#         return newTag
#     else:
#         DB_tag.tagSelected = tag.tagSelected
#         return DB_tag


# initially add tags (default status)
@router.post("/updateSeveralTags")
def initTagsInfo(tags: SeveralTags, db: Session = Depends(get_db)):
    for tag in tags.tags:
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


@router.post("/updateTagStatus")
def updateTagStatus(userID: str, tagID: str, db: Session = Depends(get_db)):
    userID = uuid.UUID(userID)
    DB_tag = db.query(DBTags).filter(DBTags.userID == userID, DBTags.tagID == tagID).first()

    if DB_tag:
        DB_tag.tagSelected = True
        db.commit()
        db.refresh(DB_tag)

        return True
    else:
        return False



@router.get("/getTags",)
# order : 0: ascending, 1: descending, other: ignore
# is_select(str) : true / false / * (all)
def getTags(userID: str, tag_type: str, order: int, is_select: str, db: Session = Depends(get_db)):
    if is_select not in ['true', 'false', "*"]:
        return None
    
    if tag_type == '*':
        DB_tags = db.query(DBTags).filter(DBTags.userID == userID).all()
    else:
        DB_tags = db.query(DBTags).filter(DBTags.userID == userID, DBTags.tagType == tag_type).all()

    if is_select != '*':
        is_select = is_select=='true'
        DB_tags = [x for x in DB_tags if x.tagSelected == is_select]

    if order == 0:
        DB_tags = sorted(DB_tags, key=lambda x: x.order)
    elif order == 1:
        DB_tags = sorted(DB_tags, key=lambda x: x.order, reverse=True)


    return DB_tags