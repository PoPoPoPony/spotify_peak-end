import request from '../utils/request'



export function getMe(accessToken) {
    let config = {
        headers: { 
            "Authorization": "Bearer " + accessToken
        },
        url: '/me/albums',
        method: 'GET',
    }

    return request(config)
}