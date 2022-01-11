import requests from '../utils/requests'


export function get_genre(token) {
    console.log(token)
    let config = {
        url: 'https://api.spotify.com/v1/recommendations/available-genre-seeds',
        method: 'GET',
        header: {
            'Authorization': 'Bearer ' + token
        }
    }
    return requests(config)
}