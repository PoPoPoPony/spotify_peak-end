import requests


baseURL = "http://ponylis.ddns.net:8080/api/v1/"


def get_users(emails:list[str] | str):
    if emails == "*":
        data = requests.get(baseURL+'user/getAllUser')
        data = data.json()
    else:
        data = []
        for email in emails:
            retv = requests.get(baseURL+'user/getUser', params={'email': email})
            data.append(retv.json())

    return data

def get_songlist_info(user_id:str, list_type:str, period:str):
    data = requests.get(baseURL+'songListInfo/getSongListInfos', params={'userID': user_id, 'listType': list_type, 'period': period})

    return data.json()

def get_songlist_score(songlist_id:str):
    data = requests.get(baseURL+'songListScore/getSongListScore', params={'songListID': songlist_id})

    return data.json()

def get_songlist_elems(songlist_id:str, rule_type: str, order:int):
    data = requests.get(baseURL+'songListElem/getSongListElems', params={'songListID': songlist_id, 'ruleType': rule_type, 'order':order})

    return data.json()
    
def get_track_infos(track_ids: list[str]):
    data = requests.get(baseURL+'trackInfo/getTrackInfos', params={'trackIDs': track_ids})

    return data.json()

def get_artist_infos(artist_ids: list[str]):
    data = requests.get(baseURL+'artistInfo/getArtistInfos', params={'artistIDs': artist_ids})

    return data.json()

def get_saved_track_infos(user_id: str):
    data = requests.get(baseURL+'userSavedTracks/getUserSavedTrackInfos', params={'userID': user_id})

    return data.json()

def get_recent_track_infos(user_id: str):
    data = requests.get(baseURL+'userRecentTracks/getUserRecentTrackInfos', params={'userID': user_id})

    return data.json()

def get_tag_infos(user_id:str, tag_type: str, order: int, is_select: str):
    data = requests.get(baseURL+'tags/getTags', params={'userID': user_id, 'tag_type':tag_type, 'order': order, 'is_select': is_select})

    return data.json()

def get_audio_features(user_id:str):
    data = requests.get(baseURL+'userAudioFeatures/getUserAudioFeatures', params={'userID': user_id})

    return data.json()
    