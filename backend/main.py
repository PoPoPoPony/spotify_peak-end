from typing import Optional
from fastapi import FastAPI
from user import user_token
import httpx
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get('/')
def root():
    return {"Hello": "World"}

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


@app.get("/show_token/{token}")
def show_token(token:str):
    print(token)
    return RedirectResponse('http://localhost:8080/tags')

client_id = '5e3c611726d54d488fb918a4c8a8739c'
URL = 'https://accounts.spotify.com/authorize?client_id=5e3c611726d54d488fb918a4c8a8739c&response_type=token&redirect_uri=http://127.0.0.1:8000/show_token/&scope=user-read-private'

URL = 'https://accounts.spotify.com/authorize'

@app.get("api/get_token/")
async def get_token():
    # async with httpx.get() as client:
    #     await client.get(URL)
    # params = {
    #     'client_id': '5e3c611726d54d488fb918a4c8a8739c',
    #     'response_type': 'token',
    #     'redirect_uri': 'http://127.0.0.1:8000/show_token/',
    #     'scope': 'user-read-private'
    # }
    headers = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}

    response = httpx.get(URL,headers=headers)
    
    print(response.next_request.url)

    
    httpx.get(response.next_request.url)


@app.get("/login/")
async def login():
    URL = "https://accounts.spotify.com/zh-TW/login?continue=https%3A%2F%2Faccounts.spotify.com%2Fauthorize"
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
    }
    response = httpx.get(URL, headers = headers)
    print(response.text)


    return {'template': response.text}
