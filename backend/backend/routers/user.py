from fastapi import APIRouter
import requests
import uuid as uuidPkg



router = APIRouter(
    prefix='api/v1/user',
    tags = ["for user init DB data"]
)

@router.get("/initUser")
def initUser(userNmae: str, ):
    pass