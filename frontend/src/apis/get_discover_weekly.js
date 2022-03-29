import request from '../utils/request'

export function GetDiscoverWeekly(accessToken) {
    let config = {
        headers: { 
            "Authorization": "Bearer " + accessToken,
        },
        url: '/search',
        method: 'GET',
        params: {
            "q": "Discover Weekly",
            "type": "playlist",
            "limit": 1
        }
    }

    return request(config)
}