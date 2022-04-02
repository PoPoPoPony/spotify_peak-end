from database import Base, engine
from models import DBUserInfo


print("Creating database...")
Base.metadata.create_all(engine)