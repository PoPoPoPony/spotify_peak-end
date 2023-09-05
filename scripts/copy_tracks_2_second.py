import requests
from typing import List
import json
import uuid


baseURL = "http://ponylis.ddns.net:8080/api/v1/"



def get_song_lst_id(user_id: str, list_type:str, period: str) -> List:
    data = requests.get(baseURL+'songListInfo/getSongListID', params={'userID': user_id, 'listType': list_type, 'period': period})

    return data.json()


def get_song_lst_elems(song_lst_id: str, rule_type: str, order: int):
    data = requests.get(baseURL+'songListElem/getSongListElems', params={'songListID': song_lst_id, 'ruleType': rule_type, 'order': order})

    return data.json()


def update_song_lst_elems(data):
    data = {"elems": data}
    # data = json.dumps(data)
    retv = requests.post(baseURL+'songListElem/updateSongListElems', json=data)

    return retv



def copy_and_set_default_tracks(user_id, first_songlist_id, second_songlist_id):
    first_elems = get_song_lst_elems(first_songlist_id, "order", "0")

    datas = []

    for first_elem in first_elems:
        trackID = first_elem['trackID']
        splendidScore = -1
        likeScore = -1
        addSongList = first_elem['addSongList']
        order = first_elem['order']
        beforeListened = first_elem['beforeListened']
        recommend = first_elem['recommend']

        data = {
            'songListID': uuid.UUID(second_songlist_id).hex,
            'userID': uuid.UUID(user_id).hex,
            'trackID': trackID,
            'splendidScore': splendidScore,
            'likeScore': likeScore,
            'addSongList': addSongList,
            'order': order,
            'beforeListened': beforeListened,
            'recommend': recommend
        }

        # data = json.dumps(data)
        datas.append(data)

    update_song_lst_elems(datas)



USER_ID='a6115442-5f81-4df6-81dd-0d28573f62d9'

FIRST_WD_SONGLISTID = get_song_lst_id(USER_ID, "Weekly_Discovery", "first")['songListID']
FIRST_T_SONGLISTID = get_song_lst_id(USER_ID, "Tags", "first")['songListID']

SECOND_WD_SONGLISTID = get_song_lst_id(USER_ID, "Weekly_Discovery", "second")['songListID']
SECOND_T_SONGLISTID = get_song_lst_id(USER_ID, "Tags", "second")['songListID']


copy_and_set_default_tracks(USER_ID, FIRST_WD_SONGLISTID, SECOND_WD_SONGLISTID)
copy_and_set_default_tracks(USER_ID, FIRST_T_SONGLISTID, SECOND_T_SONGLISTID)
