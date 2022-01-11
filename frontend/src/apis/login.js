import request from '../utils/request'


export function Login() {
    let config = {
        url: '/api/login',
        method: 'GET',
    }

    return request(config)
}