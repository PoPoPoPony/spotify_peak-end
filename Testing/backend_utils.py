import requests
from typing import List


baseURL = "http://ponylis.ddns.net:8080/api/v1/"


def get_users(email: str) -> List:
    if email == "*":
        data = requests.get(baseURL+'user/getAllUser')
    else:
        data = requests.get(baseURL+'user/getUser', params={'email': email})

    return data.json()


def get_song_lst_id(user_id: str, list_type:str, period: str) -> List:
    data = requests.get(baseURL+'songListInfo/getSongListInfo', params={'userID': user_id, 'listType': list_type, 'period': period})

    return data.json()


def get_song_lst_elems(song_lst_id: str, rule_type: str, order: int):
    data = requests.get(baseURL+'songListElem/getSongListElems', params={'songListID': song_lst_id, 'ruleType': rule_type, 'order': order})

    return data.json()


def get_song_lst_score(song_lst_id: str):
    data = requests.get(baseURL+'songListScore/getSongListScore', params={'songListID': song_lst_id})

    return data.json()

def get_tags(user_id: str, tag_type: str, is_select:str="*" ):
    data = requests.get(baseURL+'tags/getTags', params={'userID': user_id, 'tag_type': tag_type, 'order': 0, 'is_select': is_select})

    return data.json()


def get_track_infos(track_ids):
    data = requests.get(baseURL+'trackInfo/getTrackInfos', params={'trackIDs': track_ids})

    return data.json()
