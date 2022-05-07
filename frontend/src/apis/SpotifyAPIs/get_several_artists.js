import request from '../../utils/request'

export function GetSeveralArtists(accessToken, artistsIDs) {
    let config = {
        headers: { 
            "Authorization": "Bearer " + accessToken,
        },
        url: '/artists',
        method: 'GET',
        params: {
            "ids": artistsIDs
        }
    }

    return request(config)
}