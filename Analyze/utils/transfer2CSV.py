from user import User
from song import Song
from utils.utils import getUserInfos, getSongListIDs, getAllSongs, getSongTitleInfo, getArtistInfo, getSongListScore, getAllTags
from typing import List
import pandas as pd


baseURL = "http://ponyia.ddns.net:8080/api/v1/"


def transfer():
    users = []

    # 取得所有受試者
    expTypes = [f'{0}_{x}' for x in range(4)]
    expTypes.extend([f'{1}_{x}' for x in range(4)])

    userInfos = getUserInfos(expTypes=expTypes)

    for i in range(len(userInfos)):
        userID = userInfos[i]['userID']
        temp = list(getSongListIDs([userID]).values())[0]
        userInfos[i]['WD_ID'] = temp['WD_ID']
        userInfos[i]['T_ID'] = temp['T_ID']

        user = User(**userInfos[i])
        users.append(user)

    for user in users:
        WD_ID = user.WD_ID
        T_ID = user.T_ID

        WDSongListInfos, WDDeletedSongNum = getSongInfos(WD_ID)
        user.setWDSongInfos(WDSongListInfos)
        user.setWDDeletedSongNum(WDDeletedSongNum)

        TSongListInfos, TDeletedSongNum = getSongInfos(T_ID)
        user.setTSongInfos(TSongListInfos)
        user.setTDeletedSongNum(TDeletedSongNum)

        user.setSongListScores(getSongListScore(WD_ID), getSongListScore(T_ID))
        tagInfos = getAllTags(user.userID)

        for tagInfo in tagInfos:
            tagInfo.pop('userID')
            if tagInfo['tagType']=="Artists":
                tagInfo['tagID'] = getArtistInfo(tagInfo['tagID'])['artistName']
            elif tagInfo['tagType']=="Tracks":
                tagInfo['tagID'] = getSongTitleInfo(tagInfo['tagID'])['trackName']

        user.setTagInfos(tagInfos)

    # 轉換成csv格式
    email = []
    within = []
    between = []
    songListType = []
    deleteNum = []
    songTitle = []
    artist = []
    likeScore = []
    splendidScore = []
    add = []
    order = []
    songListScore = []
    tags = []

    for user in users:
        WD_len = len(user.WDsongInfos)
        T_len = len(user.TsongInfos)

        
        email.extend([user.userEmail]*(WD_len+T_len))
        within.extend([user.withinType]*(WD_len+T_len))
        between.extend([user.betweenType]*(WD_len+T_len))
        
        # WD SongScores
        songListType.extend(["Weekly discovery"]*WD_len)
        deleteNum.extend([user.WDDeletedSongNum]*WD_len)
        for song in user.WDsongInfos:
            songTitle.append(song.songTitle)
            artist.append(song.artistName)
            likeScore.append(song.likeScore)
            splendidScore.append(song.splendidScore)
            add.append(song.addSongList)
            order.append(song.order)
        songListScore.extend([user.WDScore]*WD_len)

        # T SongScores
        songListType.extend(["Tag"]*T_len)
        deleteNum.extend([user.TDeletedSongNum]*T_len)
        for song in user.TsongInfos:
            songTitle.append(song.songTitle)
            artist.append(song.artistName)
            likeScore.append(song.likeScore)
            splendidScore.append(song.splendidScore)
            add.append(song.addSongList)
            order.append(song.order)
        songListScore.extend([user.TScore]*T_len)

        tags.extend([user.tagInfos]*(WD_len+T_len))


    data = {
        "email": email,
        "withinType": within,
        "betweenType": between,
        "songListType": songListType,
        "deleteSongNum": deleteNum,
        "songTitle": songTitle,
        "artistName": artist,
        "likeScore": likeScore,
        "splendidScore": splendidScore, 
        "addToSongList": add, 
        "order": order,
        "songListScore": songListScore, 
        "tags": tags
    }

    df = pd.DataFrame(data)
    df.to_csv("preTest.csv", encoding="UTF-8", index=False)

def getSongInfos(songListID:str) -> List[Song]:
    songs = []

    allSongInfos = getAllSongs(songListID, containDelete=True)
    songInfos = [x for x in allSongInfos if x['trackShowType']=='onList']
    deleteNum = len(allSongInfos)-len(songInfos)

    for i in range(len(songInfos)):
        songID = songInfos[i].pop('trackID')
        songTitleInfo = getSongTitleInfo(songID)
        songInfos[i]["songTitle"] = songTitleInfo["trackName"]

        songInfos[i]["artistName"] = getArtistInfo(songTitleInfo['artistID'])['artistName']

        songInfos[i].pop('userID')
        songInfos[i].pop('trackShowType')
        songInfos[i].pop('songListID')

        s = Song(**songInfos[i])
        songs.append(s)

    return songs, deleteNum





