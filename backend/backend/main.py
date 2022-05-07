from typing import Optional
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, songListInfo, trackInfo, user, artists, songListElem, songListScore, tags, audioFeatures

app = FastAPI()


# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# app.include_router()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(artists.router)
app.include_router(trackInfo.router)
app.include_router(songListInfo.router)
app.include_router(songListElem.router)
app.include_router(songListScore.router)
app.include_router(tags.router)
app.include_router(audioFeatures.router)

@app.get("/")
def read_root():
    return {"Hello": "World!"}
