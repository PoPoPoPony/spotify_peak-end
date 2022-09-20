import requests
import json
from typing import List
from user import User


baseURL = "http://ponyia.ddns.net:8080/api/v1/"


def getUserInfos(expTypes: List) -> List:
    data = requests.get(baseURL+'user/getUsers', params={'expTypes': expTypes})

    return data.json()


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


def getAllSongs(songListID, containDelete=False):
    data = requests.get(baseURL+'songListElem/getAllSongs', params={'songListID': songListID, 'containDelete': containDelete})
    songs = data.json()

    return songs


def getSongTitleInfos(songIDs):
    data = requests.get(baseURL+'trackInfo/getTrackInfos', params={'trackIDs': songIDs})
    songTitleInfos = data.json()

    return songTitleInfos


def getArtistInfos(artistIDs):
    data = requests.get(baseURL+'artist/getArtistInfos', params={'artistIDs': artistIDs})
    artistInfos = data.json()

    return artistInfos


def getSongTitleInfo(songID):
    data = requests.get(baseURL+'trackInfo/getTrackInfo', params={'trackID': songID})
    songTitleInfo = data.json()

    return songTitleInfo


def getArtistInfo(artistID):
    data = requests.get(baseURL+'artist/getArtistInfo', params={'artistID': artistID})
    artistInfo = data.json()

    return artistInfo


def getAllTags(userID):
    data = requests.get(baseURL+'tags/getAllTags', params={'userID': userID})
    tagInfos = data.json()

    return tagInfos