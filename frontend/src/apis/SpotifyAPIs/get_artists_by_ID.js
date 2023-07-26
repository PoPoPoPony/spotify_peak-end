import request from '../../utils/request'

export function GetArtistsByID(accessToken, ArtistIDsStr) {
    let config = {
        headers: {
            "Authorization": "Bearer " + accessToken
        },
        url: '/artists',
        method: 'GET',
        params: {
            "ids": ArtistIDsStr
        }
    }

    return request(config)
}