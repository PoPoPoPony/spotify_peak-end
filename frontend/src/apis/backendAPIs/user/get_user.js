import request from '../../../utils/requestBackend'



export function GetUser(userEmail) {
    let config = {
        url: '/user/getUser',
        method: 'GET',
        headers: {
            "Content-Type": "application/json"
        },
        params: {
            'email': userEmail
        }
    }
    

    return request(config)
}