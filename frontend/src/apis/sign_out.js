import request from '../utils/request'


export function SignOut() {
    let config = {
        url: '/sign_out',
        method: 'GET',
    }
    
    return request(config)
}