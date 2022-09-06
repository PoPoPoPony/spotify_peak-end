class User:
    def __init__(self, userID, WD_ID, T_ID) -> None:
        self.userID = userID
        self.WD_ID = WD_ID
        self.T_ID = T_ID

    def setSongListScores(self, WDScore:int, TScore:int) -> None:
        self.WDScore = WDScore
        self.TScore = TScore

    def setWDSongScores(self, likeScores:list, dislikeScores:list, endScores:list) -> None:
        self.WDLikeScores = likeScores
        self.WDDislikeScores = dislikeScores
        self.WDEndScores = endScores


    def setTSongScores(self, likeScores:list, dislikeScores:list, endScores:list) -> None:
        self.TLikeScores = likeScores
        self.TDislikeScores = dislikeScores
        self.TEndScores = endScores

    

    