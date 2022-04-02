from email.mime import base
from email.policy import default
from enum import unique
import uuid
from database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Integer



class UserInfo(Base):
    __tablename__ = "UserInfo"
    userID = Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False, default=uuid.uuid4)
    userName = Column(String, nullable=False)
    betweenType = Column(Integer, nullable=False)
    withinType = Column(Integer, nullable=False)

    def __init__(self, userID, userName, betweenType, withinType):
        self.userID = userID
        self.userName = userName
        self.betweenType = betweenType
        self.withinType = withinType
