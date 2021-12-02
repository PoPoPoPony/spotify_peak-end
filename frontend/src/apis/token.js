import requests from '../utils/requests'


export function LoginRedirect() {
    let config = {
        url: 'http://localhost:8000/login/',
        method: 'GET',
    }
    return requests(config)
}
