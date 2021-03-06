import base64
from fastapi import APIRouter
from fastapi import Header
from fastapi.responses import RedirectResponse
import os
import requests
import uuid


router = APIRouter(
    prefix="/api/v1/auth",
    tags = ["for Spotify API auth"]
)

redirectPage = 0
betweenSubjectType = 0
withinSubjectType = 0
accessToken = ""
refreshToken = ""
userName = ""



@router.get("/SpotifyAuth")
def SpotifyAuth(redirect_page: int, between_subject_type: int, within_subject_type: int, user_name: str):
    global redirectPage
    redirectPage = redirect_page
    global betweenSubjectType
    betweenSubjectType = between_subject_type
    global withinSubjectType
    withinSubjectType = within_subject_type
    global userName
    userName = user_name

    ID = os.getenv("SPOTIFY_CLIENT_ID")
    URL = "https://accounts.spotify.com/authorize?"
    URL += "response_type=code&client_id="+ID
    URL += "&redirect_uri=http://ponyia.ddns.net:8080/api/v1/auth/SpotifyAuthCallback&scope="

    authScpoe = [
        'user-read-private',
        'user-read-email',
        'user-library-read',
        'user-read-recently-played',
        'playlist-read-private',
        'user-follow-read'
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
        "redirect_uri": "http://ponyia.ddns.net:8080/api/v1/auth/SpotifyAuthCallback",
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


    global userName
    global betweenSubjectType
    global withinSubjectType

    userID = str(uuid.uuid4())

    data = {
        "userID": userID, 
        "userName": userName,
        "betweenType": betweenSubjectType,
        "withinType": withinSubjectType
    }

    r = requests.post(url="http://ponyia.ddns.net:8080/api/v1/user/initUser", json=data)
    print(r)

    if redirectPage==0:
        redirectPageURL = 'http://ponyia.ddns.net:8081/create_list'
    else:
        redirectPageURL = 'http://ponyia.ddns.net:8081/tags'

    redirectPageURL+="?access_token=" + accessToken
    redirectPageURL+="&between_subject_type="+str(betweenSubjectType)
    redirectPageURL+="&within_subject_type="+str(withinSubjectType)
    redirectPageURL+="&pass_exp_num="+str(0)
    redirectPageURL+="&uuid="+userID

    return RedirectResponse(url=redirectPageURL)
