from database import Base, engine
from models import DBUserInfo, DBSongListInfo, DBSongListElem, DBSongListScore, DBTracksInfo, DBArtists, DBTags


print("Creating database...")
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)