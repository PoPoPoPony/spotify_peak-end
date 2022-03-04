import request from '../utils/request'

export function GetRecommendations(accessToken, genres, artists, tracks) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/recommendations',
        method: 'GET',
        params: {
            "limit": 50,
            "seed_artists": artists,
            "seed_genres": genres,
            "seed_tracks": tracks,
        }
    }

    return request(config)
}