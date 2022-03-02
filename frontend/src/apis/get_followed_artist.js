import request from '../utils/request'

export function GetFollowedArtist(accessToken) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/me/following',
        method: 'GET',
        params: {
            "type": 'artist',
            'limit': 50
        }
    }

    return request(config)
}