import request from '../../utils/request'

export function GetTracksByID(accessToken, trackIDsStr) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/tracks',
        method: 'GET',
        params: {
            "ids": trackIDsStr
        }
    }

    return request(config)
}