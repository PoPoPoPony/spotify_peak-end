import request from '../utils/request'

export function GetRecommendations(accessToken, genres, artists, tracks, score_obj) {
    var params = {
        "limit": 50,
        "seed_artists": artists,
        "seed_genres": genres,
        "seed_tracks": tracks,
    }

    for(var n in score_obj) {
        params[n] = score_obj[n]
    }
    
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/recommendations',
        method: 'GET',
        params: params,
    }

    return request(config)
}