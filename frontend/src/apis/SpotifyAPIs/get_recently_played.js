import request from '../../utils/request'

export function GetRecentlyPlayed(accessToken) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/me/player/recently-played',
        method: 'GET',
        params: {
            "limit": 50
        }
    }

    return request(config)
}