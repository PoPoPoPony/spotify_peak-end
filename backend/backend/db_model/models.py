import uuid
from .database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship



class DBUserInfo(Base):
    __tablename__ = "UserInfo"
    userID = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    userName = Column(String, nullable=False)
    betweenType = Column(Integer, nullable=False)
    withinType = Column(Integer, nullable=False)
    tracks = relationship("DBTracks", back_populates="user")
    songlist = relationship("DBSongList", back_populates="user")
    tags = relationship("DBSongList", back_populates="user")

    def __init__(self, userID, userName, betweenType, withinType):
        self.userID = userID
        self.userName = userName
        self.betweenType = betweenType
        self.withinType = withinType


class DBTracks(Base):
    __tablename__= "Tracks"
    index = Column(Integer, primary_key=True, unique=True, nullable=False)
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"))
    trackID = Column(String, nullable=False)
    trackName = Column(String, nullable=False)
    splendidScore = Column(Integer, nullable=False, default=-1)
    likeScore = Column(Integer, nullable=False, default=-1)
    artistID = Column(UUID(as_uuid=True), ForeignKey("Artists.artistID", ondelete="CASCADE"))
    user = relationship("DBUserInfo", back_populates="tracks")
    artist = relationship("Artists", back_populates="tracks")

    def __init__(self, index, userID, trackID, trackName, splendidScore, likeScore, artistID):
        self.index = index
        self.userID = userID
        self.trackID = trackID
        self.trackName = trackName
        self.splendidScore = splendidScore
        self.likeScore = likeScore
        self.artistID = artistID


class DBSongList(Base):
    __tablename__ = "SongList"
    index = Column(Integer, primary_key=True, unique=True, nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"))
    listType = Column(String, nullable=False)
    trackID = Column(String, ForeignKey("Tracks.trackID", ondelete="CASCADE"))
    # onList / outOfList / deleted 三種
    trackShowType = Column(Integer, nullable=False)
    addSongList = Column(Boolean, nullable=False)
    listScore = Column(Integer, nullable=False)
    user = relationship("DBUserInfo", back_populates="songlist")

    def __init__(self, index, userID, listType, trackID, trackShowType, addSongList, listScore):
        self.index = index
        self.userID = userID
        self.listType = listType
        self.trackID = trackID
        self.trackShowType = trackShowType
        self.addSongList = addSongList
        self.listScore = listScore


class DBTags(Base):
    __tablename__ = "Tags"
    index = Column(Integer, primary_key=True, unique=True, nullable=False)
    userId = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"))
    tagID = Column(String, nullable=False)
    tagType = Column(String, nullable=False)
    tagFreq = Column(Integer, nullable=False)
    tagShow = Column(Boolean, nullable=False)
    tagSelected = Column(Boolean, nullable=False)
    user = relationship("DBUserInfo", back_populates="tags")

    def __init__(self, index, userID, tagID, tagType, tagFreq, tagShow, tagSelected):
        self.index = index
        self.userID = userID
        self.tagID = tagID
        self.tagType = tagType
        self.tagFreq = tagFreq
        self.tagShow = tagShow
        self.tagSelected = tagSelected


class DBArtists(Base):
    __tablename__ = "Artists"
    index = Column(Integer, primary_key=True, unique=True, nullable=False)
    artistID = Column(String, nullable=False)
    artistName = Column(String, nullable=False)
    artisrGenre = Column(String, nullable=False)
    tracks = relationship("DBUserInfo", back_populates="artist")

    def __init__(self, index, artistID, artistName, artisrGenre):
        self.index = index
        self.artistID = artistID
        self.artistName = artistName
        self.artisrGenre = artisrGenre
