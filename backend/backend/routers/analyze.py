from fastapi import APIRouter
import requests
import uuid
from ..models.audioFeatures import AudioFeatures
from ..db_model.database import SessionLocal
from ..db_model.models import DBAudioFeatures
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import json
from ..Analyze.utils.utils import diffIntent


router = APIRouter(
    prefix='/api/v1/analyze',
    tags = ["analyz"]
)

def get_db():
    try:
        db = SessionLocal()
        yield db 
    finally:
        db.close()


@router.get("/diffIntent")
def getDiffIntent(db: Session = Depends(get_db)):
    diffIntent()
