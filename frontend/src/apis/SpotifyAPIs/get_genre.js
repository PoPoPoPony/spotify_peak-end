import request from '../../utils/request'



export function getMe(accessToken) {
    let config = {
        headers: { 
            "Authorization": "Bearer " + accessToken
        },
        url: '/me',
        method: 'GET',
    }

    return request(config)
}