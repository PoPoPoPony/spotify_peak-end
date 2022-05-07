import request from '../../../utils/requestBackend'



export function UpdateArtists(artistID, artistName) {
    var data = JSON.stringify({
        "artistID": artistID,
        "artistName": artistName
    });

    let config = {
        url: '/artist/updateArtist',
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        data: data
    }
    

    return request(config)
}