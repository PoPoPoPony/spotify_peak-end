import requests

from utils.utils import getUserInfos, getSongListScore, getSongListIDs
from user import User
from utils.draw import drawDiffTargetHist



baseURL = "http://ponyia.ddns.net:8080/api/v1/"

def diffIntent():
    classUsers = []
    for i in range(2):
        users = []

        # 不同搜尋目的的歌曲分數差異
        # betweenType_withinType
        expTypes = [f'{i}_{x}' for x in range(4)]
        userIDs = [x['userID'] for x in getUserInfos(expTypes)]
        temp = getSongListIDs(userIDs)

        for userID, songListIDs in temp.items():
            user = User(userID, songListIDs['WD_ID'], songListIDs['T_ID'])
            users.append(user)

        for user in users:
            WDScore = getSongListScore(user.WD_ID)
            TScore = getSongListScore(user.T_ID)
            user.setSongListScores(WDScore, TScore)
            
            ruleTypes = ['like', 'dislike', 'end']
            WDSongScores = {}
            TSongScores = {}

            for ruleType in ruleTypes:
                temp = requests.get(baseURL+'songListElem/getElemByRule', params={'songListID': user.WD_ID, 'ruleType': ruleType, 'num': 3})

                WDSongScores[ruleType+"Scores"] = temp.json()

                temp = requests.get(baseURL+'songListElem/getElemByRule', params={'songListID': user.T_ID, 'ruleType': ruleType, 'num': 3})

                TSongScores[ruleType+"Scores"] = temp.json()

            user.setWDSongScores(**WDSongScores)
            user.setTSongScores(**TSongScores)
        classUsers.append(users)
    
    drawDiffTargetHist(*classUsers)