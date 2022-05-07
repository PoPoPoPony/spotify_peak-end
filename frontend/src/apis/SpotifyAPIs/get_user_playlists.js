import request from '../../utils/request'

export function GetUserPlaylists(accessToken) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/me/playlists',
        method: 'GET',
        params: {
            "limit": 10
        }
    }

    return request(config)
}