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


@router.get("/SpotifyAuth")
def SpotifyAuth():
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

    accessToken = r['access_token']

    redirectPageURL='http://ponylis.ddns.net:8081/exercise'
    redirectPageURL+="?access_token=" + accessToken

    return RedirectResponse(url=redirectPageURL)




@router.get("/SpotifyAuth2")
def SpotifyAuth2():
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

    accessToken = r['access_token']

    redirectPageURL='http://ponylis.ddns.net:8081/second_test'
    redirectPageURL+="?access_token=" + accessToken
    
    return RedirectResponse(url=redirectPageURL)
