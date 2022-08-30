import request from '../../utils/request'

export function GetTopN(accessToken) {
    var params = {
        "time_range": 'short_term',
        "offset": 0,
        "limit": 50,
    }

    let config = {
        headers: { 
            "Authorization": "Bearer " + accessToken,
        },
        url: '/me/top/tracks',
        method: 'GET',
        params: params,
    }

    return request(config)
}