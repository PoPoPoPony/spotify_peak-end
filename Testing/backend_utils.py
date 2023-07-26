import requests
from typing import List


baseURL = "http://ponyia.ddns.net:8080/api/v1/"


def get_users(email: str) -> List:
    if email == "*":
        data = requests.get(baseURL+'user/getAllUser')
    else:
        data = requests.get(baseURL+'user/getUser', params={'email': email})

    return data.json()


def get_song_lst_id(user_id: str, list_type:str, period: str) -> List:
    data = requests.get(baseURL+'songListInfo/getSongListInfo', params={'userID': user_id, 'listType': list_type, 'period': period})

    return data.json()


def get_song_lst_elem(song_lst_id: str, rule_type: str, order: int):
    data = requests.get(baseURL+'songListElem/getElemByRule', params={'songListID': song_lst_id, 'ruleType': rule_type, 'order': order, 'num': 20})

    return data.json()


def get_song_lst_score(song_lst_id: str):
    data = requests.get(baseURL+'songListScore/getSongListScore', params={'songListID': song_lst_id})

    return data.json()

def get_tags(user_id: str, tag_type: str):
    data = requests.get(baseURL+'tags/getTags', params={'userID': user_id, 'tag_type': tag_type, 'order': 0})

    return data.json()


def get_song_name_by_ID(track_id):
    data = requests.get(baseURL+'trackInfo/getTrackInfo', params={'trackID': track_id})

    return data.json()
