import base64
from fastapi import APIRouter
from fastapi import Header
from fastapi.responses import RedirectResponse
import os
import requests

router = APIRouter(
    prefix="/api/v1/auth",
    tags = ["for Spotify API auth"]
)

redirectPage = 0
betweenSubjectType = 0
withinSubjectType = 0
accessToken = ""
refreshToken = ""


@router.get("/SpotifyAuth")
def SpotifyAuth(redirect_page: int, between_subject_type: int, within_subject_type: int):
    redirectPage = redirect_page
    betweenSubjectType = between_subject_type
    withinSubjectType = within_subject_type

    ID = os.getenv("SPOTIFY_CLIENT_ID")
    URL = "https://accounts.spotify.com/authorize?"
    URL += "response_type=code&client_id="+ID
    URL += "&redirect_uri=http://localhost:8080/api/v1/auth/SpotifyAuthCallback&scope="

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
        "redirect_uri": "http://localhost:8080/api/v1/auth/SpotifyAuthCallback",
        "grant_type": 'authorization_code'
    }
    appInfo = ID+":"+SECRET
    headers = {
        'Authorization': 'Basic '+ base64.b64encode(appInfo.encode("UTF-8")).decode()
    }

    r = requests.post(url=URL, data=data, headers=headers)

    r = r.json()

    accessToken = r['access_token']
    refreshToken = r['refresh_token']

    if redirectPage==0:
        redirectPageURL = 'http://localhost:8081/create_list'
    else:
        redirectPageURL = 'http://localhost:8081/tags'

    redirectPageURL+="?access_token=" + accessToken
    redirectPageURL+="&between_subject_type="+str(betweenSubjectType)
    redirectPageURL+="&within_subject_type="+str(withinSubjectType)
    redirectPageURL+="&pass_exp_num="+str(0)

    return RedirectResponse(url=redirectPageURL)