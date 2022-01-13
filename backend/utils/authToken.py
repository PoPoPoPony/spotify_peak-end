import spotipy
from spotipy.oauth2 import SpotifyOAuth


def auth():
    # scope = "user-follow-read"
    # sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    #     client_id='5e3c611726d54d488fb918a4c8a8739c',
    #     client_secret='d621355d46644b8fb9b1a090fc92cb48',
    #     redirect_uri='http://127.0.0.1:9090',
    #     scope=scope,
    #     open_browser=True,
    # ))
    # results = sp.current_user_followed_artists()
    
    # return results
    scope = "user-follow-read"
    # oauth = spotipy.oauth2.SpotifyOAuth(
    #     client_id='5e3c611726d54d488fb918a4c8a8739c',
    #     client_secret='d621355d46644b8fb9b1a090fc92cb48',
    #     redirect_uri='http://127.0.0.1:9090',
    #     scope=scope,
    #     open_browser=True,
    #     show_dialog=True,
    # )
    
    # oauth.get_access_token

    auth_manager = spotipy.oauth2.SpotifyOAuth(
        client_id='5e3c611726d54d488fb918a4c8a8739c',
        client_secret='d621355d46644b8fb9b1a090fc92cb48',
        redirect_uri='http://127.0.0.1:8000/api/login',
        scope=scope,
        show_dialog=True,
    )