from song import Song
from typing import List

class User:
    def __init__(self, userID, WD_ID, T_ID, userEmail=None, betweenType=None, withinType=None) -> None:
        self.userID = userID
        self.WD_ID = WD_ID
        self.T_ID = T_ID
        self.userEmail = userEmail
        self.betweenType = betweenType
        self.withinType = withinType

    def setSongListScores(self, WDScore:int, TScore:int) -> None:
        self.WDScore = WDScore
        self.TScore = TScore


    def setWDSongScores(self, likeScores:List, dislikeScores:List, endScores:List) -> None:
        self.WDLikeScores = likeScores
        self.WDDislikeScores = dislikeScores
        self.WDEndScores = endScores


    def setTSongScores(self, likeScores:List, dislikeScores:List, endScores:List) -> None:
        self.TLikeScores = likeScores
        self.TDislikeScores = dislikeScores
        self.TEndScores = endScores


    def setWDSongInfos(self, songs:List[Song]):
        self.WDsongInfos = songs


    def setTSongInfos(self, songs:List[Song]):
        self.TsongInfos = songs


    def setWDDeletedSongNum(self, num:int):
        self.WDDeletedSongNum = num

    def setTDeletedSongNum(self, num:int):
        self.TDeletedSongNum = num


    def setTagInfos(self, tagInfos:List):
        self.tagInfos = tagInfos
