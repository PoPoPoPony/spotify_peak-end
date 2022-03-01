import request from '../utils/request'

export function GetSongList(accessToken, playlist_id) {
    console.log(playlist_id, 111)
    let config = {
        headers: { 
            "Authorization": "Bearer " + accessToken
        },
        url: '/playlists/'+String(playlist_id),
        method: 'GET',

    }

    return request(config)
}