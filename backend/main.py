from typing import Optional
from fastapi import FastAPI



app = FastAPI()

@app.get('/')
def root():
    return {"Hello": "World"}


@app.get("/authorize/")
def read_user(user_id: int, q: Optional[str] = None):
    return {"token":"success"}
