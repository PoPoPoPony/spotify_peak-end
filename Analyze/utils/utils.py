import requests
import json
from typing import List
from user import User
from .draw import drawDiffTargetHist

baseURL = "http://ponyia.ddns.net:8080/api/v1/"


def diffIntent():
    classUsers = []
    for i in range(2):
        users = []

        # 不同搜尋目的的歌曲分數差異
        expTypes = [f'{i}_{x}' for x in range(4)]
        userIDs = getUserIDs(expTypes)
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




def getUserIDs(expTypes: List) -> List:
    data = requests.get(baseURL+'user/getUsers', params={'expTypes': expTypes})

    userIDs = [x['userID'] for x in data.json()]

    return userIDs


def getSongListIDs(userIDs: List) -> dict:
    store = {}
    for userID in userIDs:
        # storeIDs[userID] = []
        data = requests.get(baseURL+'songListInfo/getSongListInfo', params={'userID': userID, 'listType': 'Weekly_Discovery'})
        WD_ID = data.json()['songListID']

        data = requests.get(baseURL+'songListInfo/getSongListInfo', params={'userID': userID, 'listType': 'Tags'})
        T_ID = data.json()['songListID']

        store[userID] = {'WD_ID': WD_ID, 'T_ID': T_ID}
    
    return store

def getSongListScore(songListID):
    data = requests.get(baseURL+'songListScore/getSongListScore', params={'songListID': songListID})
    score = data.json()

    return score