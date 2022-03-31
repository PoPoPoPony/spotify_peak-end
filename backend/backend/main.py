from typing import Optional
from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth

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

@app.get("/")
def read_root():
    return {"Hello": "World!"}
