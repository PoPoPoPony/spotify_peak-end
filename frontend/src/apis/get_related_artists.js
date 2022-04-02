import request from '../utils/request'

export function GetRelatedArtist(accessToken, artistID) {

    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: 'artists/'+artistID+'/related-artists',
        method: 'GET',
    }

    return request(config)
}