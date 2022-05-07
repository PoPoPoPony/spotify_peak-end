import request from '../../utils/request'

export function GetLibraryTracks(accessToken) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/me/tracks',
        method: 'GET',
        params: {
            'limit': 50
        }
    }

    return request(config)
}