
from uuid import uuid4
from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
# from utils.authToken import auth
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from session import SessionData, verifier, set_cookie, backend
from fastapi import Depends
from uuid import UUID
import requests
from fastapi.responses import RedirectResponse
from typing import Optional


app = FastAPI()

origins = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "https://accounts.spotify.com/authorize"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/create_session/{uid}")
async def create_session(uid: str, response: Response):
    session = uuid4()
    data = SessionData(user_id=uid)

    await backend.create(session, data)
    set_cookie().attach_to_response(response, session)

    print(f"created session for {uid}")

    return f"created session for {uid}"

@app.get("/verify_session", dependencies=[Depends(set_cookie())])
async def whoami(session_data: SessionData = Depends(verifier)):
    print(session_data)
    return session_data

@app.post("/delete_session")
async def del_session(response: Response, session_id: UUID = Depends(set_cookie())):
    await backend.delete(session_id)
    set_cookie().delete_from_response(response)
    print("deleted session")
    return "deleted session"




@app.get('/')
def root():
    return {"Hello": "World"}

@app.get("/get_uid")
async def get_cookie(uid: Optional[str] = Cookie(None)):
    return {"uid": uid}


@app.get("/api/redirect2auth")
def redirect2auth():
    scope = "user-follow-read"
    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id='5e3c611726d54d488fb918a4c8a8739c',
        client_secret='d621355d46644b8fb9b1a090fc92cb48',
        redirect_uri='http://127.0.0.1:8000/api/login',
        scope=scope,
        show_dialog=True,
    )
    auth_url = auth_manager.get_authorize_url()
    print(123)
    return RedirectResponse(auth_url)


@app.get("/api/login")
def login():
    # auth()
    scope = "user-follow-read"

    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id='5e3c611726d54d488fb918a4c8a8739c',
        client_secret='d621355d46644b8fb9b1a090fc92cb48',
        redirect_uri='http://127.0.0.1:8000/api/login',
        scope=scope,
        show_dialog=True,
    )
    
    



    # res = requests.get("http://localhost:8000/verify_session", cookies={'cookie': '123'})
    # token = res['user_id'] if res.status_code == 200 else None

    # if token:
    #     # Step 3. Being redirected from Spotify auth page
    #     auth_manager.get_access_token(token)
    #     return RedirectResponse('/api/login')


    # if not auth_manager.validate_token(token):
    #     requests.post("http://localhost:8000/create_session/123")
    #     auth_url = auth_manager.get_authorize_url()
    #     return {'res': f'<h2><a href="{auth_url}">Sign in</a></h2>'}

    # spotify = spotipy.Spotify(auth_manager=auth_manager)
    # return f'<h2>Hi {spotify.me()["display_name"]}'



@app.get("/api/login2")
def login2():
    return 0

# http://127.0.0.1:8000/show_token/
# user-read-private
# @app.get("/show_token/{token_detail}")
# def show_token(token_detail: str):
#     print(1)
#     print(token_detail)
#     d = {}
#     token_detail = token_detail[1:]
#     lst = token_detail.split("&")
#     for i in lst:
#         key, value = i.split("=")
#         d[key] = value

#     return d


# @app.get("/show_token/{token}")
# def show_token(token:str):
#     print(token)
#     return RedirectResponse('http://localhost:8080/tags')

# client_id = '5e3c611726d54d488fb918a4c8a8739c'
# URL = 'https://accounts.spotify.com/authorize?client_id=5e3c611726d54d488fb918a4c8a8739c&response_type=token&redirect_uri=http://127.0.0.1:8000/show_token/&scope=user-read-private'

# URL = 'https://accounts.spotify.com/authorize'

# @app.get("api/get_token/")
# async def get_token():
    # async with httpx.get() as client:
    #     await client.get(URL)
    # params = {
    #     'client_id': '5e3c611726d54d488fb918a4c8a8739c',
    #     'response_type': 'token',
    #     'redirect_uri': 'http://127.0.0.1:8000/show_token/',
    #     'scope': 'user-read-private'
    # }
    # headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    # response = httpx.get(URL,headers=headers)
    
    # print(response.next_request.url)

    
    # httpx.get(response.next_request.url)



