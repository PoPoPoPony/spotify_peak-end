import base64
from fastapi import APIRouter
from fastapi import Header
from fastapi.responses import RedirectResponse
import os
import requests
import uuid
from random import choice


router = APIRouter(
    prefix="/api/v1/auth",
    tags = ["for Spotify API auth"]
)

redirectPage = 0
betweenSubjectType = ""
withinSubjectType = ""
accessToken = ""
refreshToken = ""
userEmail = ""
Period = ""


@router.get("/SpotifyAuth")
def SpotifyAuth(redirect_page: int, between_subject_type: str, within_subject_type: str, user_email: str, period: str):
    global redirectPage
    redirectPage = redirect_page
    global betweenSubjectType
    betweenSubjectType = between_subject_type
    global withinSubjectType
    withinSubjectType = within_subject_type
    global userEmail
    userEmail = user_email
    global Period
    Period = period

    ID = os.getenv("SPOTIFY_CLIENT_ID")
    URL = "https://accounts.spotify.com/authorize?"
    URL += "response_type=code&client_id="+ID
    URL += "&redirect_uri=http://ponylis.ddns.net:8080/api/v1/auth/SpotifyAuthCallback&scope="

    authScpoe = [
        'user-read-private',
        'user-read-email',
        'user-library-read',
        'user-read-recently-played',
        'playlist-read-private',
        'user-follow-read',
        'playlist-read-private',
        'user-top-read',
    ]

    for i in range(len(authScpoe)):
        URL+=authScpoe[i]
        if i<len(authScpoe)-1:
            URL+="+"

    return RedirectResponse(url=URL)


@router.get("/SpotifyAuthCallback")
def SpotifyAuthCallback(code: str):
    ID = os.getenv("SPOTIFY_CLIENT_ID")
    SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    URL = "https://accounts.spotify.com/api/token"

    data = {
        "code": code,
        "redirect_uri": "http://ponylis.ddns.net:8080/api/v1/auth/SpotifyAuthCallback",
        "grant_type": 'authorization_code'
    }
    appInfo = ID+":"+SECRET
    headers = {
        'Authorization': 'Basic '+ base64.b64encode(appInfo.encode("UTF-8")).decode()
    }

    r = requests.post(url=URL, data=data, headers=headers)

    r = r.json()

    global accessToken 
    accessToken = r['access_token']
    global refreshToken
    refreshToken = r['refresh_token']


    global userEmail
    global betweenSubjectType
    global withinSubjectType
    global Period

    userID = str(uuid.uuid4())

    data = {
        "userID": userID, 
        "userEmail": userEmail,
        "betweenType": betweenSubjectType,
        "withinType": withinSubjectType,
        "secondaryType": random_sencondary_type()
    }

    r = requests.post(url="http://ponylis.ddns.net:8080/api/v1/user/initUser", json=data)

    redirectPageURL='http://ponylis.ddns.net:8081/exercise'
    redirectPageURL+="?access_token=" + accessToken
    redirectPageURL+="&between_subject_type="+betweenSubjectType
    redirectPageURL+="&within_subject_type="+withinSubjectType
    redirectPageURL+="&uuid="+userID
    redirectPageURL+="&redirect_page="+str(redirectPage)
    redirectPageURL+="&period="+Period

    return RedirectResponse(url=redirectPageURL)




@router.get("/SpotifyAuth2")
def SpotifyAuth2(user_email: str, period: str):
    global userEmail
    userEmail = user_email
    global Period
    Period = period

    ID = os.getenv("SPOTIFY_CLIENT_ID")
    URL = "https://accounts.spotify.com/authorize?"
    URL += "response_type=code&client_id="+ID
    URL += "&redirect_uri=http://ponylis.ddns.net:8080/api/v1/auth/SpotifyAuthCallback2&scope="

    authScpoe = [
        'user-read-private',
        'user-read-email',
        'user-library-read',
        'user-read-recently-played',
        'playlist-read-private',
        'user-follow-read',
        'playlist-read-private',
        'user-top-read',
    ]

    for i in range(len(authScpoe)):
        URL+=authScpoe[i]
        if i<len(authScpoe)-1:
            URL+="+"

    return RedirectResponse(url=URL)


@router.get("/SpotifyAuthCallback2")
def SpotifyAuthCallback2(code: str):
    ID = os.getenv("SPOTIFY_CLIENT_ID")
    SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
    URL = "https://accounts.spotify.com/api/token"

    data = {
        "code": code,
        "redirect_uri": "http://ponylis.ddns.net:8080/api/v1/auth/SpotifyAuthCallback2",
        "grant_type": 'authorization_code'
    }
    appInfo = ID+":"+SECRET
    headers = {
        'Authorization': 'Basic '+ base64.b64encode(appInfo.encode("UTF-8")).decode()
    }

    r = requests.post(url=URL, data=data, headers=headers)
    r = r.json()

    global accessToken 
    accessToken = r['access_token']
    global refreshToken
    refreshToken = r['refresh_token']
    global Period

    res = requests.get(url='http://ponylis.ddns.net:8080/api/v1/user/getUser', params={"email": userEmail})
    userInfo = res.json()
    print(userInfo['secondaryType'])
    if userInfo['secondaryType'] in [0, 1]:
        list_type = 0
    else:
        list_type = 1

    redirectPageURL='http://ponylis.ddns.net:8081/second_test'
    redirectPageURL+="?access_token=" + accessToken
    redirectPageURL+="&userID="+str(userInfo['userID'])
    redirectPageURL+="&list_type="+ str(list_type) # 0, 1先做WD，2, 3先做Tag
    redirectPageURL+="&period="+Period
    redirectPageURL+="&secondaryType="+str(userInfo['secondaryType'])
    

    return RedirectResponse(url=redirectPageURL)


def random_sencondary_type():
    res = requests.get(url='http://ponylis.ddns.net:8080/api/v1/user/getAllUser')
    res = res.json()
    secondary = [x['secondaryType'] for x in res]
    d = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
    }
    for s in secondary:
        d[s]+=1

    candidate = []
    for group in d.keys():
        if d[group] == min(d.values()):
            candidate.append(group)

    return choice(candidate)
