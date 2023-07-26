import uuid
from .database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship



class DBUserInfo(Base):
    __tablename__ = "UserInfo"
    userID = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    userEmail = Column(String, nullable=False)
    betweenType = Column(Integer, nullable=False)
    withinType = Column(Integer, nullable=False)
    secondaryType = Column(Integer, nullable=False)

    tags = relationship("DBTags", back_populates="user")
    songListInfo = relationship("DBSongListInfo", back_populates="user")
    songListElem = relationship("DBSongListElem", back_populates="user")
    userAudioFeatures = relationship("DBUserAudioFeatures", back_populates="user")
    listScore = relationship("DBSongListScore", back_populates="user")
    userSavedTracks = relationship("DBUserSavedTracks", back_populates="user")
    userRecentTracks = relationship("DBUserRecentTracks", back_populates="user")

    def __init__(self, userID, userEmail, betweenType, withinType, secondaryType):
        self.userID = userID
        self.userEmail = userEmail
        self.betweenType = betweenType
        self.withinType = withinType
        self.secondaryType = secondaryType


class DBTracksInfo(Base):
    __tablename__= "TracksInfo"
    trackID = Column(String, nullable=False, primary_key=True, unique=True)
    trackName = Column(String, nullable=False)
    artistID = Column(String, ForeignKey("ArtistsInfo.artistID", ondelete="CASCADE"), nullable=False)
    popularity = Column(Integer, nullable=False)

    acousticness = Column(Float, nullable=False)
    danceability = Column(Float, nullable=False)
    energy = Column(Float, nullable=False)
    instrumentalness = Column(Float, nullable=False)
    key = Column(Integer, nullable=False)
    liveness = Column(Float, nullable=False)
    loudness = Column(Float, nullable=False)
    mode = Column(Integer, nullable=False)
    speechiness = Column(Float, nullable=False)
    tempo = Column(Float, nullable=False)
    timeSignature = Column(Integer, nullable=False)
    valence = Column(Float, nullable=False)
    preview = Column(String, nullable=True)

    artist = relationship("DBArtistsInfo", back_populates="trackInfo")
    songListElem = relationship("DBSongListElem", back_populates="trackInfo")
    userSavedTracks = relationship("DBUserSavedTracks", back_populates="trackInfo")
    userRecentTracks = relationship("DBUserRecentTracks", back_populates="trackInfo")

    def __init__(self, trackID, trackName, artistID, popularity, acousticness, danceability, energy, instrumentalness, key, liveness, loudness, mode, speechiness, tempo, timeSignature, valence, preview):
        self.trackID = trackID
        self.trackName = trackName
        self.artistID = artistID
        self.popularity = popularity

        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.instrumentalness = instrumentalness
        self.key = key
        self.liveness = liveness
        self.loudness = loudness
        self.mode = mode
        self.speechiness = speechiness
        self.tempo = tempo
        self.timeSignature = timeSignature
        self.valence = valence
        self.preview = preview

class DBSongListInfo(Base):
    __tablename__ = "SongListInfo"
    songListID = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"))
    # Weekly_Discovery or Tags
    listType = Column(String, nullable=False)
    period = Column(String, nullable=False)

    user = relationship("DBUserInfo", back_populates="songListInfo")
    listScore = relationship("DBSongListScore", back_populates="songListInfo")
    songListElem = relationship("DBSongListElem", back_populates="songListInfo")

    def __init__(self, songListID, userID, listType, period):
        self.songListID = songListID
        self.userID = userID
        self.listType = listType
        self.period = period


class DBSongListElem(Base):
    __tablename__ = "SongListElem"
    songListID = Column(UUID(as_uuid=True), ForeignKey("SongListInfo.songListID", ondelete="CASCADE"), primary_key=True, nullable=False, default=uuid.uuid4)
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"))
    trackID = Column(String, ForeignKey("TracksInfo.trackID", ondelete="CASCADE"), nullable=False, primary_key=True)

    splendidScore = Column(Integer, nullable=False, default=-1)
    likeScore = Column(Integer, nullable=False, default=-1)
    addSongList = Column(Boolean, nullable=False)
    order = Column(Integer, nullable=False)
    beforeListened = Column(Boolean, nullable=False)
    recommend = Column(String, nullable=False)

    user = relationship("DBUserInfo", back_populates="songListElem")
    trackInfo = relationship("DBTracksInfo", back_populates="songListElem")
    songListInfo = relationship("DBSongListInfo", back_populates="songListElem")

    def __init__(self, songListID, userID, trackID, splendidScore, likeScore, addSongList, order, beforeListened, recommend):
        self.songListID = songListID
        self.userID = userID
        self.trackID = trackID
        self.splendidScore = splendidScore
        self.likeScore = likeScore
        self.addSongList = addSongList
        self.order = order
        self.beforeListened = beforeListened
        self.recommend = recommend



class DBSongListScore(Base):
    __tablename__ = "SongListScore"
    songListID = Column(UUID(as_uuid=True), ForeignKey("SongListInfo.songListID", ondelete="CASCADE"), primary_key=True, unique=True, nullable=False)
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"))
    satisfyScore = Column(Integer, nullable=False)
    diversityScore = Column(Integer, nullable=False)
    noveltyScore = Column(Integer, nullable=False)
    
    songListInfo = relationship("DBSongListInfo", back_populates="listScore")
    user = relationship("DBUserInfo", back_populates="listScore")

    def __init__(self, songListID, userID, satisfyScore, diversityScore, noveltyScore):
        self.songListID = songListID
        self.userID = userID
        self.satisfyScore = satisfyScore
        self.diversityScore = diversityScore
        self.noveltyScore = noveltyScore


class DBTags(Base):
    __tablename__ = "Tags"
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"), primary_key=True)
    tagID = Column(String, nullable=False , primary_key=True)
    tagType = Column(String, nullable=False)
    tagFreq = Column(Integer, nullable=False)
    order = Column(Integer, nullable=False)
    tagSelected = Column(Boolean, nullable=False)

    user = relationship("DBUserInfo", back_populates="tags")

    def __init__(self, userID, tagID, tagType, tagFreq, order, tagSelected):
        self.userID = userID
        self.tagID = tagID
        self.tagType = tagType
        self.tagFreq = tagFreq
        self.order = order
        self.tagSelected = tagSelected


class DBArtistsInfo(Base):
    __tablename__ = "ArtistsInfo"
    artistID = Column(String, nullable=False, primary_key=True, unique=True)
    artistName = Column(String, nullable=False)
    popularity = Column(Integer, nullable=False)
    genres = Column(String, nullable=True)

    trackInfo = relationship("DBTracksInfo", back_populates="artist")

    def __init__(self, artistID, artistName, popularity, genres):
        self.artistID = artistID
        self.artistName = artistName
        self.popularity = popularity
        self.genres = genres


class DBUserAudioFeatures(Base):
    __tablename__ = "UserAudioFeatures"
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"), primary_key=True)
    minAcousticness = Column(Float, nullable=False)
    targetAcousticness = Column(Float, nullable=False)
    maxAcousticness = Column(Float, nullable=False)
    minDanceability = Column(Float, nullable=False)
    targetDanceability = Column(Float, nullable=False)
    maxDanceability = Column(Float, nullable=False)
    minEnergy = Column(Float, nullable=False)
    targetEnergy = Column(Float, nullable=False)
    maxEnergy = Column(Float, nullable=False)
    minInstrumentalness = Column(Float, nullable=False)
    targetInstrumentalness = Column(Float, nullable=False)
    maxInstrumentalness = Column(Float, nullable=False)
    minKey = Column(Integer, nullable=False)
    targetKey = Column(Integer, nullable=False)
    maxKey = Column(Integer, nullable=False)
    minLiveness = Column(Float, nullable=False)
    targetLiveness = Column(Float, nullable=False)
    maxLiveness = Column(Float, nullable=False)
    minTempo = Column(Float, nullable=False)
    targetTempo = Column(Float, nullable=False)
    maxTempo = Column(Float, nullable=False)
    minValence = Column(Float, nullable=False)
    targetValence = Column(Float, nullable=False)
    maxValence = Column(Float, nullable=False)

    user = relationship("DBUserInfo", back_populates="userAudioFeatures")

    def __init__(self, userID, minAcousticness, targetAcousticness, maxAcousticness, minDanceability, targetDanceability, maxDanceability, minEnergy, targetEnergy, maxEnergy, minInstrumentalness, targetInstrumentalness, maxInstrumentalness, minKey, targetKey, maxKey, minLiveness, targetLiveness, maxLiveness, minTempo, targetTempo, maxTempo, minValence, targetValence, maxValence):
        self.userID = userID
        self.minAcousticness= minAcousticness
        self.targetAcousticness = targetAcousticness
        self.maxAcousticness = maxAcousticness
        self.minDanceability = minDanceability
        self.targetDanceability = targetDanceability
        self.maxDanceability = maxDanceability
        self.minEnergy = minEnergy
        self.targetEnergy = targetEnergy
        self.maxEnergy = maxEnergy
        self.minInstrumentalness = minInstrumentalness
        self.targetInstrumentalness = targetInstrumentalness
        self.maxInstrumentalness = maxInstrumentalness
        self.minKey = minKey
        self.targetKey = targetKey
        self.maxKey = maxKey
        self.minLiveness = minLiveness
        self.targetLiveness = targetLiveness
        self.maxLiveness = maxLiveness
        self.minTempo = minTempo
        self.targetTempo = targetTempo
        self.maxTempo = maxTempo
        self.minValence = minValence
        self.targetValence = targetValence
        self.maxValence = maxValence




class DBUserSavedTracks(Base):
    __tablename__ = "UserSavedTracks"
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"), primary_key=True)
    trackID = Column(String, ForeignKey("TracksInfo.trackID", ondelete="CASCADE"), nullable=False, primary_key=True)
    
    user = relationship("DBUserInfo", back_populates="userSavedTracks")
    trackInfo = relationship("DBTracksInfo", back_populates="userSavedTracks")

    def __init__(self, userID, trackID):
        self.userID = userID
        self.trackID = trackID


class DBUserRecentTracks(Base):
    __tablename__ = "UserRecentTracks"
    userID = Column(UUID(as_uuid=True), ForeignKey("UserInfo.userID", ondelete="CASCADE"), primary_key=True)
    trackID = Column(String, ForeignKey("TracksInfo.trackID", ondelete="CASCADE"), nullable=False, primary_key=True)
    times = Column(Integer, nullable=False)
    
    user = relationship("DBUserInfo", back_populates="userRecentTracks")
    trackInfo = relationship("DBTracksInfo", back_populates="userRecentTracks")

    def __init__(self, userID, trackID, times):
        self.userID = userID
        self.trackID = trackID
        self.times = times