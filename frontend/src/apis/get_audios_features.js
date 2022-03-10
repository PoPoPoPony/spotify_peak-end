import request from '../utils/request'

export function GetAudiosFeatures(accessToken, songIDs) {
    let config = {
        headers: { 
            "Authorization": "Bearer " + accessToken,
        },
        url: '/audio-features',
        method: 'GET',
        params: {
            "ids": songIDs
        }
    }

    return request(config)
}