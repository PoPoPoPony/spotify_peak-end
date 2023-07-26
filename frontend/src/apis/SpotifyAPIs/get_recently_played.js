import request from '../../utils/request'

export function GetRecentlyPlayed(accessToken, unix_time) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/me/player/recently-played',
        method: 'GET',
        params: {
            "limit": 50,
            'after': unix_time
        }
    }

    return request(config)
}