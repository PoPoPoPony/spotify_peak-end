import request from '../../utils/request'

export function GetSavedTracks(accessToken, offset) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/me/tracks',
        method: 'GET',
        params: {
            "limit": 50,
            'offset': offset
        }
    }

    return request(config)
}