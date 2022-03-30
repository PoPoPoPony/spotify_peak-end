from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
<<<<<<< HEAD
    return {"Hello": "World10"}
=======
    return {"Hello": "World6"}
>>>>>>> d98c88417cacf1ac826ce12084565da154810c21


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}