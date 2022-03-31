from fastapi import APIRouter
from fastapi import Header
from fastapi.responses import RedirectResponse
import os

router = APIRouter(
    prefix="/api/v1/auth",
    tags = ["for Spotify API auth"]
)

redirectPage = 0
betweenSubjectType = 0
withinSubjectType = 0


@router.get("/SpotifyAuth")
def SpotifyAuth(redirect_page: int, between_subject_type: int, within_subject_type: int):
    redirectPage = redirect_page
    betweenSubjectType = between_subject_type
    withinSubjectType = within_subject_type

    ID = os.getenv("SPOTIFY_CLIENT_ID")
    URL = "https://accounts.spotify.com/authorize?"
    URL += "response_type=code&client_id="+ID
    URL += "&redirect_uri=http://localhost:8080/api/v1/auth/SpotifyAuthCallback&scpoe="

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

    # authOptions = {
    #     'url': 'https://accounts.spotify.com/api/token',
    #     'form': {
    #         "grant_type": 'authorization_code',
    #         "code": authCode,
    #         "http://localhost:8080/api/v1/auth/SpotifyAuthCallback"
    #     }
        
    # }

    return code